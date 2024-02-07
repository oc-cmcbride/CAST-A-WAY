import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.transform import Rotation

# stop wrapping my matrices dangit
np.set_printoptions(linewidth=100)

# Function definitions
def matMul(vec, mat):
    x, y, z = None, None, None
    if(vec.ndim == 1):
        x = vec[0]
        y = vec[1]
        z = vec[2]
    elif(vec.ndim == 2):
        x = vec[:, 0]
        y = vec[:, 1]
        z = vec[:, 2]
    
    nx = x * mat[0][0] + y * mat[1][0] + z * mat[2][0] + mat[3][0]
    ny = x * mat[0][1] + y * mat[1][1] + z * mat[2][1] + mat[3][1]
    nz = x * mat[0][2] + y * mat[1][2] + z * mat[2][2] + mat[3][2]

    w  = x * mat[0][3] + y * mat[1][3] + z * mat[2][3] + mat[3][3]

    # remove zeros
    if(vec.ndim == 1 and w == 0):
        w = 0
    elif(vec.ndim == 2):
        w[w == 0] = 1

    nx = nx / w
    ny = ny / w
    nz = nz / w

    return np.vstack([nx, ny, nz]).T

def translate(vec, dx, dy, dz):
    x, y, z = None, None, None
    if(vec.ndim == 1):
        x = vec[0]
        y = vec[1]
        z = vec[2]
    elif(vec.ndim == 2):
        x = vec[:, 0]
        y = vec[:, 1]
        z = vec[:, 2]

    nx = x + dx
    ny = y + dy
    nz = z + dz
    return np.vstack([nx, ny, nz]).T

# Meters per Foot (exact)
mpft = 2.54 * 12 / 100

# Get image parameters
imgIndex = 1
frame = cv2.imread(f'{imgIndex:04}.png')
dimensions = frame.shape
height = dimensions[0]
width = dimensions[1]

# DEFINE PARAMETERS
# CAMERA SETTINGS

fov = 48.4555 # Degrees

# I think these don't really matter?
Znear = 0.1
Zfar = 1000

# Camera position
# World Coordinates
camX =  0   * mpft
camY = -1   * mpft
camZ =  3.2 * mpft

# only have pitch right now; camera shouldn't have roll (gross) and yaw can be reanalyzed as just a different position
# Could add yaw if you need it; implement into rot below
camPitch = -150 #degrees

# LASER SETTINGS
lasSep = -0.5 * mpft # This is that b thingy
lasYaw = 8.8 #degrees

# Calculations - Shouldn't need to change

# Camera Matrix
a = width/height
fCalc = 1 / np.tan(np.deg2rad(fov / 2))

C = np.array([[fCalc,         0,                                0, 0],
              [    0, a * fCalc,                                0, 0],
              [    0,         0,            Zfar / (Zfar - Znear), 1],
              [    0,         0, -(Zfar * Znear) / (Zfar - Znear), 0]])

# Rotation
rot = Rotation.from_euler('x', camPitch, degrees = True)

# Unit vector in direction of laser
lasDir = Rotation.from_euler('y', lasYaw, degrees = True).apply(np.array([0, 0, 1]))
lasDir = lasDir / lasDir[2] # Normalize depth

# 2 points for depth calc line (there's maybe a better mathy way to do this but eh)
d1 = 1 * mpft
d2 = 2 * mpft
lasRef1 = matMul((lasDir * d1) + np.array([lasSep, 0, 0]), C)
lasRef2 = matMul((lasDir * d2) + np.array([lasSep, 0, 0]), C)
u1 = lasRef1[0][0]
u2 = lasRef2[0][0]
# depth inverses
di1 = 1 / d1
di2 = 1 / d2

# Curve fit with numpy - 1st degree polynomial = line
depthFit = np.polynomial.Polynomial.fit([u1, u2], [di1, di2], 1)
# print(f"Numpy fit: {depthFit}")

# Blur radius - must be odd
brad = 21
threshold = 70

stripHeight = 10

# Rotation per Frame
rotPerFrame = 10 #degrees
rpf = Rotation.from_euler('z', rotPerFrame, degrees = True)

# print(f'Camera properties: {width}, {height}')

if height % stripHeight != 0:
    print("stripHeight is not a factor of height; problems will probably happen")
    exit()

# Number of strips to process
stripCount = int(height/stripHeight)
# Each measured point
cameraPoints = [None] * stripCount

fullThing = None

#cv2.namedWindow("Window")

while frame is not None:

    # make a backup for display
    displayImage = frame
    
    # Separate color channels to get red because eevee rendering no realistic
    (B, G, R) = cv2.split(frame)
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Blur to reduce noise
    gray = cv2.GaussianBlur(R, (brad, 1), 0)

    for i in range(stripCount):
        # crop to strip - numpy does rows and columns instead of x and y because ¯\_(ツ)_/¯
        strip = gray[stripHeight * i : stripHeight * (i + 1), :]
        
        # decimate y axis
        strip = cv2.resize(strip, (width, 1), interpolation = cv2.INTER_AREA)

        # Find brightest point
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(strip)
        # print(f"location: {str(maxLoc)}\tvalue: {maxVal}")

        xLoc = maxLoc[0]

        if(maxVal > threshold):
            cameraPoints[i] = (float(xLoc), stripHeight * (i + 0.5))
            displayImage = cv2.circle(frame, [round(cameraPoints[i][0]), round(cameraPoints[i][1])], 3, (100, 255, 100), -1)
            #displayImage = cv2.putText(frame, f'{pixelToDistance(maxLoc[0])} cm', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 1, 2)
        else:
            cameraPoints[i] = None
    
    #cv2.imshow("Window", displayImage)

    # Remove Nones
    uvPoints = np.array(list(filter(lambda item: item is not None, cameraPoints)))
    # Normalize coordinates
    uvPoints[:, 0] = 2 * uvPoints[:, 0] / width - 1
    uvPoints[:, 1] = 2 * uvPoints[:, 1] / height - 1

    # START: REAL MATH FOR 3D DATA EXTRACTION

    # To solve for the rays, we'll need to append a depth
    # I like one
    unos = np.ones([uvPoints.shape[0], 1])
    uvA = np.hstack([uvPoints, unos])

    # We can just do the multiplication by the inverse camera matrix!
    recon = matMul(uvA, np.linalg.inv(C))

    # There's probably a better way of doing this
    # ChatGPT gave me something that don't work :(
    for i in range(recon.shape[0]):
        # Normalize Z axis for EZ math later
        recon[i, :] = recon[i, :] / recon[i, 2]

    # Calculate depths
    # print(uvPoints[:, 0])
    D = 1 / depthFit(uvPoints[:, 0])

    # These will be our points reconstructed from the image coordinates, camera matrix, and depths
    # Since we normalized the Z axis we can just multiply by the measured distance and get it good!
    # That other equation I derived in the notebook before? don't need it here :D
    derivedPoints = recon * D[:, np.newaxis]

    # Now we just reverse the earlier transformations
    derivedPoints = translate(rot.apply(derivedPoints), camX, camY, camZ)
    
    # Plot the thing
    '''
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(derivedPoints[:, 0], derivedPoints[:, 1], derivedPoints[:, 2], '-o')
    #ax.plot(camX, camY, camZ, '-o')
    #ax.plot(lasPos[0], lasPos[1], lasPos[2], '-o')
    #ax.plot(lasInt[0], lasInt[1], lasInt[2], '-x')
    ax.set_xlim(-1   * mpft, 1   * mpft)
    ax.set_ylim(-1   * mpft, 1   * mpft)
    ax.set_zlim(-0.2 * mpft, 1.8 * mpft)
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Z (m)")
    # Set the plot title and grid
    ax.set_title("Reconstruction")
    ax.grid(True)
    plt.show()
    '''

    if fullThing is None:
        fullThing = derivedPoints
    else:
        fullThing = np.vstack([derivedPoints, rpf.apply(fullThing)])


    
    imgIndex = imgIndex + 1
    frame = cv2.imread((f'{imgIndex:04}.png'))

# Plot the thing
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(fullThing[:, 0], fullThing[:, 1], fullThing[:, 2], '.', markersize = 0.5)
ax.set_xlim(-1   * mpft, 1   * mpft)
ax.set_ylim(-1   * mpft, 1   * mpft)
ax.set_zlim(-0.2 * mpft, 1.8 * mpft)
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_zlabel("Z (m)")
ax.set_title("Reconstruction")
ax.grid(True)
plt.show()

cv2.destroyAllWindows()