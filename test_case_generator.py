from PIL import Image
import imageio
import numpy as np
import random
import math
#########################################################################################################
def create_base_image_film(n):
    '''
    Create a np array of size (n,n) filled with all ones
    Input Parameters : n -> Size of the np array to be created
    Output : base_image -> 2D np array of size (n,n) 
    '''
    base_image = np.ones((n,n))
    return base_image
#########################################################################################################
def save_the_image(inp_img, img_type):
    '''
    Saves the inp_image as a bitmap image file
    Input Parameters : inp_ing (np array which is to be saved)
                       img_type ('normal image' or 'dye image')
    Output : None
    '''
    imageio.imwrite('test_case_' + img_type + '.bmp', (255 * inp_img).astype('uint8'))
#########################################################################################################
def generate_neighbours(x,y,n):
    '''
    Generates neighbour for a given input point
    Input Parameters : (x,y) -> Point for which neighbours are to be found
                       n -> size of the grid
    Output : nei (list of neighbours)
    '''
    nei = []
    if x+1 < n and y+1<n:
        nei.append((x+1,y+1))
    if x-1>=0 and y+1<n:
        nei.append((x-1,y+1))
    if x-1>=0 and y-1>=0:
        nei.append((x-1,y-1))
    if x+1<n and y-1>=0:
        nei.append((x+1,y-1))
    
    return nei
#########################################################################################################
def check_inside_circle(cx,cy,r,x,y):
    '''
    Checks if a point is inside a given circle
    Input Parameters : (cx,cy) -> center of the circle
                       r (radius of the circle)
                       (x,y) -> Point to be checked if it is inside the circle or not
    Output : Returns a boolean value indicating if the point is inside the given circle
    '''
    if (cx-x)**2 + (cy-y)**2 <= r*r:
        return True
    else:
        return False
#########################################################################################################
def create_normal_image(n):
    '''
    Creates image of the microorganism under normal microscope
    Input Parameters : n (size of the image nxn)
    Output : (cx,cy) represents center coordinates of the circle created 
             r (radius of the circle)
             filename (name of the bmp file where the image is stored)
    '''
    normal_image = create_base_image_film(n)
    seen = set()
    cy = random.randint(0,n-2)
    cx = random.randint(0,n-2)
    fill_ratio = random.randint(25,40)
    r = math.sqrt((fill_ratio * n * n) / (math.pi * 100))
    q = []
    filled = 0

    ## create a random sized circle somewhere on the white film
    for x in range(n):
        for y in range(n):
            if r*r >= (cx-x)**2 + (cy-y)**2 >= r*r-40:
                    q.append((x,y))
                    seen.add((x,y))
            if check_inside_circle(cx,cy,r,x,y):
                normal_image[x][y] = 0
                filled+=1
                seen.add((x,y))

    fill_ratio = fill_ratio * 1.00001

    ## consider the circle boundary
    ## expand the circle boundary in random directions to form amoeba like pattern
    while q and n*n*fill_ratio/100 > filled:
        curr_x, curr_y = q.pop(0)
        normal_image[curr_x][curr_y] = 0
        filled+=1
        neighbours = generate_neighbours(curr_x, curr_y, n)
        unseen_neigbhours = []
        for it in neighbours:
            if it not in seen:
                unseen_neigbhours.append(it)

        s = len(unseen_neigbhours)
        #randomly drop a neighbour
        if s >=2:
            drop_index = random.randint(0,s-1)
            unseen_neigbhours.remove(unseen_neigbhours[drop_index])

        for it in unseen_neigbhours:
            seen.add(it)
            q.append(it)
        
    img_type_for_saving = 'normal_image'
    save_the_image(normal_image, img_type_for_saving)
    print("Normal Microscope image generated. Parasite coverage = " + str(fill_ratio) + "%")
    return int(cx),int(cy),int(r), 'test_case_'+img_type_for_saving+'.bmp'
#########################################################################################################
def create_dye_sensor_image(n,cx,cy,r):
    '''
    Creates image of the veins observed under dye sensor
    Input Parameters : n (size of the image nxn)
                      (cx,cy) -> representing the center coordinates of the circle in normal microscope image
                      r -> representing radius of the circle in normal microscope image
    Output : dye_image (created image of the veins)
             filename (name of the bmp file where the image is stored)
    '''
    dye_image = create_base_image_film(n)

    #idea is to randomly draw lines in rows and cols
    fill_ratio = random.randint(0,15)
    filled = 0

    r1 = random.randint(0,80)
    r2 = random.randint(r1,80)

    ## 'r1'% of lines are vertical
    ## drawn within close range of the area where the parasite is present in normal microscope image
    while (n*n*fill_ratio*r1/(100*100)) > filled:
        x1 = random.randint(max(0, cx-r),min(n-1,cx+r)) 
        y1 = random.randint(max(0, cy-r),min(n-1, cy+r))
        y2 = random.randint(max(0, cy-r), min(n-1, cy+r))

        for y in range(min(y1,y2),max(y1,y2)):
            if dye_image[x1][y] == 1:
                dye_image[x1][y] = 0
                filled+=1

    ## 'r2'% of the lines are horizontal
    ## drawn within close range of the area where the parasite is present in normal microscope image
    while (n*n*fill_ratio*r2/(100*100)) > filled:
        x1 = random.randint(max(0, cx-r),min(n-1,cx+r)) 
        y1 = random.randint(max(0, cy-r),min(n-1, cy+r))
        x2 = random.randint(x1,min(n-1, cx+r))

        for x in range(min(x1,x2),max(x1,x2)):
            if dye_image[x][y1] == 1:
                dye_image[x][y1] = 0
                filled+=1

    ## randomly draw vertical and horizontal lines anywhere on the film
    while (n*n*fill_ratio/100) > filled:
        nums = random.randint(0,2)
        if nums == 1:
            x1 = random.randint(0,n-1) 
            y1 = random.randint(0,n-1)
            y2 = random.randint(0,n-1)

            for y in range(min(y1,y2),max(y1,y2)):
                if dye_image[x1][y] == 1:
                    dye_image[x1][y] = 0
                    filled+=1

        else:
            x1 = random.randint(0,n-1) 
            y1 = random.randint(0,n-1)
            x2 = random.randint(0,n-1)

            for x in range(min(x1,x2),max(x1,x2)):
                if dye_image[x][y1] == 1:
                    dye_image[x][y1] = 0
                    filled+=1
        
    img_type_for_saving = 'dye_image'
    save_the_image(dye_image, img_type_for_saving)
    print("Dye Microscope image generated. Veins coverage = " + str((filled/(n*n))*100) + "%")
    return dye_image, 'test_case_'+img_type_for_saving+'.bmp'
#########################################################################################################
def generate_test_case(size):
    '''
    Generates a test case pair (normal microscope image, dye sensor image)
    Input Parameters : size (size of the image to be creates) (images are of resolution size x size)
    Output : normal_file_location (location of the bmp file of the created normal microscope image)
             dye_file_location (location of the bmp file of the created dye sensor image)
    '''
    print("#########################################################################")
    print("Test Case Generation started")
    print("Started Generating Normal Microscope image")
    cx,cy,r, normal_file_location = create_normal_image(size)
    print("Started Generating Dye Sensor image")
    img, dye_file_location = create_dye_sensor_image(size,cx,cy,r)
    print("#########################################################################")
    return normal_file_location, dye_file_location