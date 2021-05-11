#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import multiprocessing
import os                                                               
 
# Creating the tuple of all the processes
all_processes = ('dna_checker.py', '2_4Ghz_switch.py', 'random_quickguest.py')                                    
                                                  
# This block of code enables us to call the script from command line.                                                                                
def execute(process):                                                             
    os.system(f'python3 {process}')                                       
                                                                                
                                                                                
process_pool = multiprocessing.Pool(processes = 1)                                                        
process_pool.map(execute, all_processes)