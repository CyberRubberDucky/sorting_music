import random
import pygame
import numpy as np
import time
import matplotlib.pyplot as plt

pygame.mixer.init()

def play_sound(value):
    min_freq = 400
    max_freq = 2000
    frequency = min_freq + (max_freq - min_freq) * (value / 100)
    duration = 0.1
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    sine_wave = np.sin(2 * np.pi * frequency * t)
    audio_data = np.int16(sine_wave * 32767)
    stereo_audio_data = np.column_stack((audio_data, audio_data))
    sound = pygame.sndarray.make_sound(stereo_audio_data)
    sound.play()

def bubble_sort(arr, print_array, play_sound, ax, algorithm_name):
    n = len(arr)
    start_time = time.time()
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                current_time = time.time() - start_time
                print_array(arr, j, j+1, ax, algorithm_name, current_time)
                play_sound(arr[j])
                time.sleep(0.05)
    current_time = time.time() - start_time
    print_array(arr, -1, -1, ax, algorithm_name, current_time)

def selection_sort(arr, print_array, play_sound, ax, algorithm_name):
    n = len(arr)
    start_time = time.time()
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        current_time = time.time() - start_time
        print_array(arr, i, min_idx, ax, algorithm_name, current_time)
        play_sound(arr[i])
        time.sleep(0.05)
    current_time = time.time() - start_time
    print_array(arr, -1, -1, ax, algorithm_name, current_time)

def insertion_sort(arr, print_array, play_sound, ax, algorithm_name):
    start_time = time.time()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        current_time = time.time() - start_time
        print_array(arr, j + 1, i, ax, algorithm_name, current_time)
        play_sound(arr[i])
        time.sleep(0.05)
    current_time = time.time() - start_time
    print_array(arr, -1, -1, ax, algorithm_name, current_time)

def merge(arr, start, mid, end, print_array, play_sound, ax, algorithm_name):
    left = arr[start:mid + 1]
    right = arr[mid + 1:end + 1]
    i = j = 0
    k = start

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        current_time = time.time() - start_time
        print_array(arr, k, -1, ax, algorithm_name, current_time)
        play_sound(arr[k])
        k += 1
        time.sleep(0.05)

    while i < len(left):
        arr[k] = left[i]
        i += 1
        current_time = time.time() - start_time
        print_array(arr, k, -1, ax, algorithm_name, current_time)
        play_sound(arr[k])
        k += 1
        time.sleep(0.05)

    while j < len(right):
        arr[k] = right[j]
        j += 1
        current_time = time.time() - start_time
        print_array(arr, k, -1, ax, algorithm_name, current_time)
        play_sound(arr[k])
        k += 1
        time.sleep(0.05)

def merge_sort(arr, print_array, play_sound, ax, algorithm_name):
    global start_time
    start_time = time.time()

    def _merge_sort(arr, start, end):
        if start >= end:
            return

        mid = (start + end) // 2
        _merge_sort(arr, start, mid)
        _merge_sort(arr, mid + 1, end)
        merge(arr, start, mid, end, print_array, play_sound, ax, algorithm_name)

    _merge_sort(arr, 0, len(arr) - 1)
    current_time = time.time() - start_time
    print_array(arr, -1, -1, ax, algorithm_name, current_time)

def print_array(arr, sorted_index, moved_index, ax, algorithm_name=None, time_taken=None):
    print("\033c", end="")
    if algorithm_name and time_taken is not None:
        print(f"{algorithm_name} - Time: {time_taken:.2f} sec ({time_taken*1000:.2f} ms)")
    else:
        print("Sorting Visualization...")
    for i, val in enumerate(arr):
        if i == sorted_index:
            print(f"[{val}]", end=" ")
        elif i == moved_index:
            print(f"({val})", end=" ")
        else:
            print(f" {val} ", end=" ")
    print("\n" + "-" * 50)
    ax.clear()
    ax.bar(range(len(arr)), arr, color='white', edgecolor='black')
    ax.bar(sorted_index, arr[sorted_index], color='yellow', edgecolor='black')
    ax.bar(moved_index, arr[moved_index], color='purple', edgecolor='black')
    ax.set_title(f"{algorithm_name if algorithm_name else 'Sorting Visualization'} - "
                 f"Time: {time_taken if time_taken is not None else 0:.2f} sec "
                 f"({time_taken*1000 if time_taken is not None else 0:.2f} ms)")
    ax.set_facecolor('black')
    plt.pause(0.01)

def run_sorting_algorithms():
    pygame.init()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sorting_algorithms = [merge_sort, bubble_sort, selection_sort, insertion_sort]
    
    while True:
        arr = list(range(1, 101))
        random.shuffle(arr)
        for sort_func in sorting_algorithms:
            arr_copy = arr[:]
            sort_func(arr_copy, print_array, play_sound, ax, sort_func.__name__)

run_sorting_algorithms()
