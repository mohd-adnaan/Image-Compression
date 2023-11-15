from compress_and_store_image import deserialize_slow
from compress_and_store_image import serialize_slow
import time

normal_count = 0
dye_count = 0
start_time = 0
end_time = 0
normal_count_fast = 0
dye_count_fast = 0
start_time_fast = 0
end_time_fast = 0
#########################################################################################################
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
def find_colored_area(input_tree):
    '''
    Finds number of black pixels under the given Quad() subtree
    Input Parameters : input_tree (Quad() for which number of black pixels is to be counted)
    Output : Number of black pixels
    '''
    if input_tree == None or input_tree.region_type=="pure_white":
        return 0

    elif input_tree.region_type == "pure_black":
        return (input_tree.end_row+1 - input_tree.start_row) * (input_tree.end_col+1 - input_tree.start_col)

    else:
        return find_colored_area(input_tree.tl) + find_colored_area(input_tree.tr) + find_colored_area(input_tree.bl) + find_colored_area(input_tree.br)
#########################################################################################################
def find_overlap_slow(normal_quad_tree, dye_quad_tree):
    '''
    Finds overlap of black pixels in two quad trees
    Input Parameters : normal_quad_tree (Quad tree of normal microscope image)
                       dye_quad_tree (Quad tree of dye microscope)
    Output : None
    '''
    global normal_count
    global dye_count
    global start_time
    global end_time

    start_time = time.time()
    ## if mircoscopre quad tree is empty there is no overalp
    if normal_quad_tree is None or normal_quad_tree.region_type == "pure_white":
        return

    ## if normal microscope quad tree is pure black
    ## overlap is number of black nodes in dye quad tree
    elif normal_quad_tree.region_type == "pure_black":
        normal_count+=find_colored_area(normal_quad_tree)
        if dye_quad_tree.region_type == "pure_black":
            dye_count+=find_colored_area(dye_quad_tree)
            
        elif dye_quad_tree.region_type == "pure_white":
            return

        else: 
            dye_count+=find_colored_area(dye_quad_tree)


    ## if normal microscope quad tree is impure
    ## overlap is the set of nodes that are black both in normal_quad_tree and dye_quad_tree
    elif normal_quad_tree.region_type == "impure":
        if dye_quad_tree.region_type == "pure_black":
            ans = find_colored_area(normal_quad_tree)
            normal_count+=ans
            dye_count+=ans
        elif dye_quad_tree.region_type == "pure_white":
            normal_count+=find_colored_area(normal_quad_tree)
        else: 
            find_overlap_slow(normal_quad_tree.tl, dye_quad_tree.tl)
            find_overlap_slow(normal_quad_tree.tr, dye_quad_tree.tr)
            find_overlap_slow(normal_quad_tree.bl, dye_quad_tree.bl)
            find_overlap_slow(normal_quad_tree.br, dye_quad_tree.br)
    
    
    return
#########################################################################################################
def find_overlap_fast(normal_quad_tree, dye_quad_tree):
    '''
    Finds overlap of black pixels in two quad trees using the deserialization_fast
    Input Parameters : normal_quad_tree (Quad tree of normal microscope image)
                       dye_quad_tree (Quad tree of dye microscope)
    Output : None
    '''
    global normal_count_fast
    global dye_count_fast
    global start_time_fast
    global end_time_fast

    start_time_fast = time.time()
    ## if mircoscopre quad tree is empty there is no overalp
    if normal_quad_tree is None or normal_quad_tree.region_type[0] == "pure_white":
        return
    
    ## if normal microscope quad tree is pure black
    ## overlap is number of black nodes in dye quad tree
    elif normal_quad_tree.region_type[0] == "pure_black":
        normal_count_fast+=normal_quad_tree.region_type[1]
        if dye_quad_tree.region_type[0] == "pure_black":
            dye_count_fast+=dye_quad_tree.region_type[1]
        
        elif dye_quad_tree.region_type[0] == "pure_white":
            return

        else: 
            dye_count_fast+=dye_quad_tree.region_type[1]

    ## if normal microscope quad tree is impure
    ## overlap is the set of nodes that are black both in normal_quad_tree and dye_quad_tree
    elif normal_quad_tree.region_type[0] == "impure":
        if dye_quad_tree.region_type[0] == "pure_black":
            normal_count_fast+=normal_quad_tree.region_type[1]
            dye_count_fast+=normal_quad_tree.region_type[1]
        elif dye_quad_tree.region_type[0] == "pure_white":
            normal_count_fast+=normal_quad_tree.region_type[1]
        else: 
            find_overlap_fast(normal_quad_tree.tl, dye_quad_tree.tl)
            find_overlap_fast(normal_quad_tree.tr, dye_quad_tree.tr)
            find_overlap_fast(normal_quad_tree.bl, dye_quad_tree.bl)
            find_overlap_fast(normal_quad_tree.br, dye_quad_tree.br)
    
    
    return
#########################################################################################################
def get_stats_slow():
    '''
    Gets the Stats of the find_overlap_slow
    Input Parameters : None
    Output : percent of dye in microorganisms body, execution time of the find_overlap_slow function
    '''
    global normal_count
    global dye_count
    global start_time
    global end_time

    end_time = time.time()
    return (dye_count/normal_count) * 100, end_time - start_time
#########################################################################################################
def get_stats_fast():
    '''
    Gets the Stats of the find_overlap_fast
    Input Parameters : None
    Output : percent of dye in microorganisms body, execution time of the find_overlap_slow function
    '''
    global normal_count_fast
    global dye_count_fast
    global start_time_fast
    global end_time_fast

    end_time_fast = time.time()
    return (dye_count_fast/normal_count_fast) * 100, end_time_fast - start_time_fast
#########################################################################################################