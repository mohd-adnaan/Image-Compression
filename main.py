from test_case_generator import generate_test_case
from compress_and_store_image import compress_images
from compress_and_store_image import decompress_images
from find_overlap import find_overlap_slow, find_overlap_fast
from find_overlap import get_stats_slow, get_stats_fast
import time

input_image_size = 1000
start_time = 0
end_time = 0
############################################################################################################
## generate the test case
normal_img, dye_image = generate_test_case(input_image_size) 

############################################################################################################
## compress the normal microscope image
print("Started Image Compression")
print('Started Compressing the normal image')
cmp_normal_image = compress_images(normal_img, 'normal_image')
print('Normal image compressed and stored as : ', cmp_normal_image)
print('Started Compressing the dye image')
## compress the dye sensor image
cmp_dye_image = compress_images(dye_image, 'dye_image')
print('Dye image compressed and stored as : ', cmp_dye_image)
print("#########################################################################")

############################################################################################################
#### WORKING ON SLOW EXECUTION
## decompress the image
start_time = time.time()
print('Started working on slow execution')
print('Started Decompressing the saved encrypted images')
normal_quad_tree, dye_quad_tree = decompress_images(cmp_normal_image, cmp_dye_image, input_image_size, 'slow')
print('Decompression complete')
## find the overlap between two images
print('Started finding overlap between two images')
find_overlap_slow(normal_quad_tree, dye_quad_tree)
infected_ratio, exec_slow_time = get_stats_slow()
if infected_ratio > 10:
    print('Parasite has cancer. Body dye percent is ' + str(infected_ratio) + '%')
else:
    print('Parasite does not have cancer. Body dye percent is ' + str(infected_ratio) + '%')
end_time = time.time()
print("Slow Code execution time :", exec_slow_time)
print("#########################################################################")

############################################################################################################
#### WORKING ON FAST EXECUTION
start_time = time.time()
print('Started working on fast execution')
print('Started Decompressing the saved encrypted images')
normal_quad_tree, dye_quad_tree = decompress_images(cmp_normal_image, cmp_dye_image, input_image_size, 'fast')
print('Decompression complete')
## find the overlap between two images
print('Started finding overlap between two images')
find_overlap_fast(normal_quad_tree, dye_quad_tree)
infected_ratio, exec_fast_time = get_stats_fast()
if infected_ratio > 10:
    print('Parasite has cancer. Body dye percent is ' + str(infected_ratio) + '%')
else:
    print('Parasite does not have cancer. Body dye percent is ' + str(infected_ratio) + '%')
end_time = time.time()
print("Fast Code execution time :", exec_fast_time)
print("#########################################################################")
############################################################################################################