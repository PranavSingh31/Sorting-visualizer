import pygame
import random

SCREEN_WIDTH = 910
SCREEN_HEIGHT = 750
arr_size = 130
rect_size = 7

arr = []
barr = []

pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
renderer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

complete = False

def init():
    global window, renderer
    success = True
    try:
        window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        renderer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    except pygame.error as e:
        print("Couldn't create window:", e)
        success = False
    return success

def close():
    pygame.quit()

def visualize(x=-1, y=-1, z=-1):
    renderer.fill((0, 0, 0))

    for j in range(len(arr)):
        rect = pygame.Rect(j * rect_size, 0, rect_size, arr[j])
        if complete:
            pygame.draw.rect(renderer, (100, 180, 100), rect, 1)
        elif j == x or j == z:
            pygame.draw.rect(renderer, (100, 180, 100), rect)
        elif j == y:
            pygame.draw.rect(renderer, (165, 105, 189), rect)
        else:
            pygame.draw.rect(renderer, (170, 183, 184), rect)

    window.blit(renderer, (0, 0))
    pygame.display.flip()

# 0. Generate Array

def load_arr():
    global arr
    arr = barr.copy()

def randomize_and_save_array():
    global barr
    barr = [random.randint(0, SCREEN_HEIGHT) for _ in range(arr_size)]

# SORTING ALGORITHMS START HERE

# 1. Selection Sort
def selection_sort():
    for i in range(arr_size - 1):
        min_index = i
        for j in range(i + 1, arr_size):
            if arr[j] < arr[min_index]:
                min_index = j
                visualize(i, min_index)
            pygame.time.delay(1)
        arr[i], arr[min_index] = arr[min_index], arr[i]

# 2. Insertion Sort
def insertion_sort():
    for i in range(1, arr_size):
        j = i - 1
        temp = arr[i]
        while j >= 0 and arr[j] > temp:
            arr[j + 1] = arr[j]
            j -= 1
            visualize(i, j + 1)
            pygame.time.delay(5)
        arr[j + 1] = temp

# 3. Bubble Sort
def bubble_sort():
    for i in range(arr_size - 1):
        for j in range(arr_size - 1 - i):
            if arr[j + 1] < arr[j]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                visualize(j + 1, j, arr_size)
            pygame.time.delay(1)

# 4. Merge Sort
def merge_two_sorted_arrays(arr, si, ei):
    size_output = (ei - si) + 1
    output = [0] * size_output

    mid = (si + ei) // 2
    i, j, k = si, mid + 1, 0
    while i <= mid and j <= ei:
        if arr[i] <= arr[j]:
            output[k] = arr[i]
            visualize(i, j)
            i += 1
            k += 1
        else:
            output[k] = arr[j]
            visualize(i, j)
            j += 1
            k += 1

    while i <= mid:
        output[k] = arr[i]
        visualize(-1, i)
        i += 1
        k += 1

    while j <= ei:
        output[k] = arr[j]
        visualize(-1, j)
        j += 1
        k += 1

    for l in range(si, ei + 1):
        arr[l] = output[l - si]
        visualize(l)
        pygame.time.delay(15)

def merge_sort(arr, si, ei):
    if si >= ei:
        return
    mid = (si + ei) // 2
    merge_sort(arr, si, mid)
    merge_sort(arr, mid + 1, ei)
    merge_two_sorted_arrays(arr, si, ei)

# 5. QUICK SORT
def partition_array(arr, si, ei):
    count_small = 0
    for i in range(si + 1, ei + 1):
        if arr[i] <= arr[si]:
            count_small += 1

    c = si + count_small
    arr[c], arr[si] = arr[si], arr[c]
    visualize(c, si)

    i, j = si, ei

    while i < c and j > c:
        if arr[i] <= arr[c]:
            i += 1
        elif arr[j] > arr[c]:
            j -= 1
        else:
            arr[i], arr[j] = arr[j], arr[i]
            visualize(i, j)
            pygame.time.delay(70)
            i += 1
            j -= 1

    return c

def quick_sort(arr, si, ei):
    if si >= ei:
        return

    c = partition_array(arr, si, ei)
    quick_sort(arr, si, c - 1)
    quick_sort(arr, c + 1, ei)


# 6. HEAP SORT
def inplace_heap_sort(input_list):
    n = len(input_list)
    for i in range(1, n):
        child_index = i
        parent_index = (child_index - 1) // 2

        while child_index > 0:
            if input_list[child_index] > input_list[parent_index]:
                input_list[child_index], input_list[parent_index] = input_list[parent_index], input_list[child_index]
            else:
                break

            visualize(parent_index, child_index)
            pygame.time.delay(40)

            child_index = parent_index
            parent_index = (child_index - 1) // 2

    for heap_last in range(n - 1, 0, -1):
        input_list[0], input_list[heap_last] = input_list[heap_last], input_list[0]

        parent_index = 0
        left_child_index = 2 * parent_index + 1
        right_child_index = 2 * parent_index + 2

        while left_child_index < heap_last:
            max_index = parent_index

            if input_list[left_child_index] > input_list[max_index]:
                max_index = left_child_index
            if right_child_index < heap_last and input_list[right_child_index] > input_list[max_index]:
                max_index = right_child_index
            if max_index == parent_index:
                break

            input_list[parent_index], input_list[max_index] = input_list[max_index], input_list[parent_index]

            visualize(max_index, parent_index, heap_last)
            pygame.time.delay(40)

            parent_index = max_index
            left_child_index = 2 * parent_index + 1
            right_child_index = 2 * parent_index + 2


def execute():
    if not init():
        print("SDL Initialization Failed.")
        return

    randomize_and_save_array()
    load_arr()

    quit = False
    while not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
                complete = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quit = True
                    complete = False
                    print("\nEXITING SORTING VISUALIZER.")
                elif event.key == pygame.K_0:
                    randomize_and_save_array()
                    complete = False
                    load_arr()
                    print("\nNEW RANDOM LIST GENERATED.")
                elif event.key == pygame.K_1:
                    load_arr()
                    print("\nSELECTION SORT STARTED.")
                    complete = False
                    selection_sort()
                    complete = True
                    print("\nSELECTION SORT COMPLETE.")
                elif event.key == pygame.K_2:
                    load_arr()
                    print("\nINSERTION SORT STARTED.")
                    complete = False
                    insertion_sort()
                    complete = True
                    print("\nINSERTION SORT COMPLETE.")
                elif event.key == pygame.K_3:
                    load_arr()
                    print("\nBUBBLE SORT STARTED.")
                    complete = False
                    bubble_sort()
                    complete = True
                    print("\nBUBBLE SORT COMPLETE.")
                elif event.key == pygame.K_4:
                    load_arr()
                    print("\nMERGE SORT STARTED.")
                    complete = False
                    merge_sort(arr, 0, arr_size - 1)
                    complete = True
                    print("\nMERGE SORT COMPLETE.")
                elif event.key == pygame.K_5:
                    load_arr()
                    print("\nQUICK SORT STARTED.")
                    complete = False
                    quick_sort(arr, 0, arr_size - 1)
                    complete = True
                    print("\nQUICK SORT COMPLETE.")
                elif event.key == pygame.K_6:
                    load_arr()
                    print("\nHEAP SORT STARTED.")
                    complete = False
                    inplace_heap_sort(arr)
                    complete = True
                    print("\nHEAP SORT COMPLETE.")

        visualize()
        clock.tick(60)

def controls():
    print("WARNING: Giving repetitive commands may cause latency and the visualizer may behave unexpectedly. Please give a new command only after the current command's execution is done.\n")
    print("Available Controls inside Sorting Visualizer:")
    print("    Use 0 to Generate a different randomized list.")
    print("    Use 1 to start Selection Sort Algorithm.")
    print("    Use 2 to start Insertion Sort Algorithm.")
    print("    Use 3 to start Bubble Sort Algorithm.")
    print("    Use 4 to start Merge Sort Algorithm.")
    print("    Use 5 to start Quick Sort Algorithm.")
    print("    Use 6 to start Heap Sort Algorithm.")
    print("    Use q to exit out of Sorting Visualizer\n")
    print("PRESS ENTER TO START SORTING VISUALIZER...\n")
    print("Or type -1 to quit the program.")

    user_input = input()
    if user_input == "-1":
        return False
    return True

def intro():
    print("==============================Sorting Visualizer==============================\n")
    print("Visualization of different sorting algorithms in Python with Pygame Library. A sorting algorithm is an algorithm that puts the elements of a list in a certain order. While there are a large number of sorting algorithms, in practical implementations a few algorithms predominate.\n")
    print("In this implementation of sorting visualizer, we'll be looking at some of these sorting algorithms and visually comprehend their working.\n")
    print("The sorting algorithms covered here are Selection Sort, Insertion Sort, Bubble Sort, Merge Sort, Quick Sort and Heap Sort.\n")
    print("The list size is fixed to 130 elements. You can randomize the list and select any type of sorting algorithm to call on the list from the given options. Here, all sorting algorithms will sort the elements in ascending order. The sorting time being visualized for an algorithm is not exactly the same as their actual time complexities. The relatively faster algorithms like Merge Sort, etc. have been delayed so that they could be properly visualized.\n")
    input("Press ENTER to show controls...")

def main():
    intro()

    while True:
        print()
        if controls():
            execute()
        else:
            print("\nEXITING PROGRAM.")
            break

    close()

if __name__ == '__main__':
    main()
