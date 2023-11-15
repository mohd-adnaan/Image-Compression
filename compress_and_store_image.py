import time
import sys
import imageio

## region_type -> pure_black(all black), pure_white(all white), impure(black and white)
class Quad():
    '''
    Datastructure to store the black and white image
    '''
    def __init__(self, start_row, start_col, end_row, end_col, region_type, tl=None, tr=None, bl=None, br=None):
        self.start_row = start_row  ## start row of the Quad()
        self.start_col = start_col  ## start col of the Quad()
        self.end_row = end_row  ## end row of the Quad()
        self.end_col = end_col  ## end col of the Quad()
        self.region_type = region_type  ## pure_white, pure_black, impure
        self.tl = tl  ## top left box
        self.tr = tr  ## top right box
        self.bl = bl  ## bottom left box
        self.br = br  ## bottom right box
#########################################################################################################
def create_quad_tree(img, start_row, start_col, end_row, end_col):
    '''
    Creates a quad tree for the input image
    Input Parameters : img (Input image which is to be converted into quad tree)
                       (start_row, start_col) <-> (end_row, end_col) (indicate the part of the image to be converted into quadtree)
    Output : Quad() (Created Quad tree for the input image 'img')
    '''
    if start_row>end_row or start_col>end_col:
        return None
    
    black = False
    white = False

    for r in range(start_row, end_row+1):
        for c in range(start_col, end_col+1):
            if black and white:
                break
            elif not black and img[r][c] == 0:
                black = True
            elif not white and img[r][c] == 255:
                white = True
    if black and not white: ## node is purely black no need to break further
        return Quad(start_row, start_col, end_row, end_col, "pure_black")
    elif white and not black: ## node is purely white no need to break further
        return Quad(start_row, start_col, end_row, end_col, "pure_white")
    ## node is not pure, break it further
    new_node = Quad(start_row, start_col, end_row, end_col, "impure")
    mid_row = (start_row + end_row)//2
    mid_col = (start_col + end_col)//2

    new_node.tl = create_quad_tree(img, start_row, start_col, mid_row, mid_col)
    new_node.tr = create_quad_tree(img, start_row, mid_col+1, mid_row, end_col)
    new_node.bl = create_quad_tree(img, mid_row+1, start_col, end_row, mid_col)
    new_node.br = create_quad_tree(img, mid_row+1, mid_col+1, end_row, end_col)

    return new_node
#########################################################################################################
def serialize_slow(tree):
    '''
    Serializes the Quad Tree such that it can be stored in a file
    Input Paramaters : tree (Input Quad Tree to be serialized)
    Output : Serialized output of the input Quad Tree 'tree'
    '''
    if tree == None:
        return '3'
    if tree.region_type == "pure_black":
        return '0'
    if tree.region_type == 'pure_white':
        return '1'
    else:
        ans = '2'
        ans+=serialize_slow(tree.tl)
        ans+=serialize_slow(tree.tr)
        ans+=serialize_slow(tree.bl)
        ans+=serialize_slow(tree.br)
        return ans
#########################################################################################################
def deserialize_slow(tree, start_row, start_col, end_row, end_col):
    '''
    Deserialize the stored serialized string to obtain back the Quad Tree
    Input Parameters : tree (Serialized string input)
                       (start_row, start_col) <-> (end_row, end_col) (indicate the part of the image which is currently being deserialized)

    Output : Quad() representing root of the Quad tree of the entire image
    '''
    global indx
    if indx >= len(tree):
        return None
    curr_val = tree[indx]
    if curr_val == '3':
        return None
    if curr_val == '0':
        new_node = Quad(start_row, start_col, end_row, end_col, 'pure_black')
    if curr_val == '1':
        new_node = Quad(start_row, start_col, end_row, end_col, 'pure_white')
    if curr_val == '2':
        new_node = Quad(start_row, start_col, end_row, end_col, 'impure')
        mid_row = (start_row+end_row)//2
        mid_col = (start_col + end_col)//2
        indx+=1
        new_node.tl = deserialize_slow(tree, start_row, start_col, mid_row, mid_col)
        indx+=1
        new_node.tr = deserialize_slow(tree, start_row, mid_col+1, mid_row, end_col)
        indx+=1
        new_node.bl = deserialize_slow(tree, mid_row+1, start_col, end_row, mid_col)
        indx+=1
        new_node.br = deserialize_slow(tree, mid_row+1, mid_col+1, end_row, end_col)

    return new_node
#########################################################################################################
def deserialize_fast(tree, start_row, start_col, end_row, end_col):
    '''
    Deserialize the stored serialized string to obtain back the Quad Tree
    region_type of a Quad now represents ['pure_black'/'pure_white'/'impure', #black nodes in the current Quad]
    Deserializing the tree in such a way would prevent calculating number of black nodes for each Quad subtree
    Input Parameters : tree (Serialized string input)
                       (start_row, start_col) <-> (end_row, end_col) (indicate the part of the image which is currently being deserialized)

    Output : Quad() representing root of the Quad tree of the entire image
    '''
    global indx
    if indx >= len(tree):
        return None
    curr_val = tree[indx]
    if curr_val == '3':
        return None
    if curr_val == '0':
        new_node = Quad(start_row, start_col, end_row, end_col, ['pure_black', (end_row-start_row+1) * (end_col-start_col+1)])
    if curr_val == '1':
        new_node = Quad(start_row, start_col, end_row, end_col, ['pure_white',0])
    if curr_val == '2':
        new_node = Quad(start_row, start_col, end_row, end_col, ['impure',0])
        mid_row = (start_row+end_row)//2
        mid_col = (start_col + end_col)//2
        indx+=1
        new_node.tl = deserialize_fast(tree, start_row, start_col, mid_row, mid_col)
        if new_node.tl!=None:
            new_node.region_type[1]+=new_node.tl.region_type[1]

        indx+=1
        new_node.tr = deserialize_fast(tree, start_row, mid_col+1, mid_row, end_col)
        if new_node.tr!=None:
            new_node.region_type[1]+=new_node.tr.region_type[1]

        indx+=1
        new_node.bl = deserialize_fast(tree, mid_row+1, start_col, end_row, mid_col)
        if new_node.bl!=None:
            new_node.region_type[1]+=new_node.bl.region_type[1]

        indx+=1
        new_node.br = deserialize_fast(tree, mid_row+1, mid_col+1, end_row, end_col)
        if new_node.br!=None:
            new_node.region_type[1]+=new_node.br.region_type[1]

    return new_node

#########################################################################################################
def save_to_file(ans, file_type):
    '''
    Saves a given string to a text file
    Input Parameters : ans (input string to be store to a file)
                       file_type (suffix of the text file name)
    Output : file_name (Name of the text file where the string was stored)
    '''
    file_name = 'compressed_'+file_type + '.txt'

    text_file = open(file_name, 'w')
    text_file.write(ans)
    text_file.close()
    return file_name

#########################################################################################################
def compress_images(file_name, file_type):
    '''
    Compresses the image to store it efficiently. Uses serialize function
    Input Parameters : file_name (bmp file name of the image to be compressed)
                       file_type ('normal_image' OR 'dye_image')
    Output : file_name (Name of the text file where the image is stored after compression)
    '''
    img = imageio.imread(file_name)
    m = len(img)
    n = len(img[0])

    ## create the quad tree
    quad_tree = create_quad_tree(img, 0 , 0, m-1, n-1)
    
    ## serialize the quad tree (compress the quad tree)
    compressed_quad_tree = serialize_slow(quad_tree)

    ## save the quad tree to text file
    file_name = save_to_file(compressed_quad_tree +'\n' +str(n), file_type)
    return file_name

#########################################################################################################
def decompress_images(normal_cmp_image, dye_cmp_image, size, execution_type):
    '''
    Decompress the stored text file for the image
    Input Parameters : normal_cmp_image (image under normal microscope)
                       dye_cmp_image (dye image microscope)
                       size (size of the original image)    
                       execution_type (slow/fast execution)

    Output : None
    '''
    global indx
    indx = 0
    with open(normal_cmp_image) as f:
        normal_img_content = f.readlines()
        
    if execution_type == 'slow':
        normal_quad_tree = deserialize_slow(normal_img_content[0], 0, 0,int(normal_img_content[1])-1, int(normal_img_content[1])-1)
    else:
        normal_quad_tree = deserialize_fast(normal_img_content[0], 0, 0,int(normal_img_content[1])-1, int(normal_img_content[1])-1)


    
    indx = 0
    with open(dye_cmp_image) as f:
        dye_image_content = f.readlines()

    if execution_type == 'slow':
        dye_quad_tree = deserialize_slow(dye_image_content[0], 0, 0, int(dye_image_content[1])-1, int(dye_image_content[1])-1)
    else:
        dye_quad_tree = deserialize_fast(dye_image_content[0], 0, 0, int(dye_image_content[1])-1, int(dye_image_content[1])-1)

    return normal_quad_tree, dye_quad_tree

indx = 0
#########################################################################################################