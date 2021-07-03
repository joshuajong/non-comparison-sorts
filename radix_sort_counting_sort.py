"""
Student ID: 31190863

This module consists of the main functions for FIT2004 S1/2021 Assignment 1 and additional
helper functions. This module is organised in a way that main functions precede helper
functions (each labelled to show which main function uses it).
"""
# main function for Task 1
def best_interval(transactions, t):
    """ This function takes in as input, a list of non-negative integers (transactions) 
        and a size of interval t; and finds the interval of size t containing the most 
        number of elements from transactions with the minimum start time. 
        :input: an unsorted list of non-negative integers, transactions of length N and;
                a non-negative integer, t representing the size of the interval chosen
        :output: a tuple, (best_t, count), called retval, where best_t is the minimum start time 
                 for the interval containing the most number of elements from transactions and 
                 count is the number of elements from transactions within the interval
        :time complexity: best and worst case is O(kN), dominated by radix_sort_int. 
                          The while loop in the code runs in O(N) time.
                          N is the length of the input list, transactions, while k is the maximum 
                          number of digits of any element in transactions.
                          Calculation: O(kN) + O(N) = O(kN)
        :aux space complexity: O(kN) due to function call to radix_sort_int;
                               counting the elements in the interval and pointers i and j take 
                               constant space O(1)
        :space complexity: O(kN) as our input list is length (N) * maximum number of digits (k)
        While loop complexity: The pointer j only needs to count every element once. This 
                               is because when the i pointer is incremented to the next element, 
                               the previous count variable is reused. The only time that the 
                               count needs to be reset is if the next element was not counted 
                               when the previous element was the start of the interval, giving the 
                               while loop O(N) time complexity
    """
    retval = (0, 0)
    i = 0
    j = 0
    # prev_i is used to remember the last position of the i pointer 
    prev_i = 0
    count = 0
    if len(transactions) == 0:
        return retval
    transactions = radix_sort_int(transactions) # this is O(kN) time
    max_item = transactions[-1]
    # max_val holds current max value for any interval in each iteration
    max_val = transactions[0]
    while i < len(transactions) and j < len(transactions): # this is O(N) time
        # skip duplicate elements
        if transactions[prev_i] == transactions[i] and prev_i != i:
            i += 1
        # break early if previous element in the iteration covers an interval up to (including)
        # the last element in the list
        elif (transactions[i-1] + t) > max_item and i > 0:
            break 
        else:
            # reset count and j if starting a new interval from element at transactions[i]
            if prev_i != i:
                # if next element is part of interval of previous element, count is reused
                if transactions[i] <= transactions[prev_i]+t:
                    count = count - (i - prev_i)
                    prev_i = i
                else:
                    count = 0
                    prev_i = i
            # if current value is less than current interval ending endpoint
            if transactions[j] <= (transactions[i] + t):
                count += 1
                max_val = transactions[j]
                j += 1  
            else:
                i += 1
            # update retval when new count is greater and the j pointer has reached
            # endpoint of one interval or end of the list
            if count > retval[1] and (prev_i != i or j == len(transactions)): 
                retval = (max_val-t, count)
    # if best_t value falls below 0 then set the best_t to 0
    if retval[0] < 0:
        return (0, retval[1])
    else:
        return retval

# main function for Task 2
def words_with_anagrams(list1, list2):
    """ This function returns the words in list1 which have anagrams in list2. All strings 
        in list1 and list2 are sorted using radix sort alphabetically (duplicates are also 
        removed in list2 for efficiency) and then compared to find the anagrams of list1 
        appearing in list2
        :input: list1 and list2 of lengths L1 and L2 respectively and
                the longest string in each are M1 and M2 respectively
        :output: a list of words in list1 which have anagrams in list2
        :time complexity: best and worst case is O(L1*M1 + L2*M2) since both lists are sorted 
                          using radix_sort_words
                          Calculation: O(L2*M2) + O(L2*M2) + O(L2*M2) + O(L1*M1) + O(L1*M1) +
                                       O(min(L1,L2)*M1) = O(L1M1 + L2M2)
        :aux space complexity: O(L1*M1 + L2*M2) due to radix_sort_words on both lists;
                               temp_list1, sorted_list1, word_pos take O(L1) space;
                               ret_list takes O(L1) space at most;
        :space complexity: O(L1*M1 + L2*M2) as input is of length L1 and L2 and the longest string
                           is M1 and M2 respectively
    """
    # handle empty list cases
    if len(list1) == 0 or len(list2) == 0:
        return []
    # sort words in list2 into anagrams
    for i in range(len(list2)):  # this is O(L2*M2) time
        list2[i] = sort_word(list2[i])
    # sort list2 in alphabetical order and remove the duplicates    
    sorted_list2 = radix_sort_words(list2)[0]  # this is O(L2*M2) time
    sorted_list2_uq = remove_duplicates(sorted_list2)  # this is O(L2*M2) time
    temp_list1 = list1[:]
    # sort words in list1 into anagrams
    for i in range(len(list1)): # this is O(L1*M1) time
        list1[i] = sort_word(list1[i])
    words_pos = radix_sort_words(list1) # this is O(L1*M1) time
    sorted_list1 = words_pos[0] 
    word_pos = words_pos[1]
    # pointer j is for list1 and i is for list2
    i = 0
    j = 0
    ret_list = []
    # this entire loop is O(min(L1,L2)*M1) time but if it is L2*M1 where the loop terminates
    # earlier, we will know that L2 < L1 so L1*M1 (from radix sort) is more significant
    # while if it is L1*M1, then it is just equal to the complexity of the radix sort
    # applied to list1 above;
    # string comparisons are done in O(M1) time since comparison will stop one it reaches 
    # the end of the string in L1
    while j < len(sorted_list1): # this is O(L1) time
        # when the i pointer reaches the end of list2 then break
        if i == len(sorted_list2_uq):
            break
        else:
            if len(sorted_list1[j]) == len(sorted_list2_uq[i]):
                # this is O(M1)
                if sorted_list1[j] == sorted_list2_uq[i]:
                    ret_list.append(temp_list1[word_pos[j]])
                    j += 1
                elif sorted_list1[j] < sorted_list2_uq[i]:
                    j += 1
                else:
                    i += 1
            else:
                # this is O(M1)
                if sorted_list1[j] < sorted_list2_uq[i]:
                    j += 1
                else:
                    i += 1
    return ret_list

# this function is used by both Task 1 and Task 2
def counting_sort_index(new_list):
    """ This function takes an unsorted list of non-negative integers as input and returns 
        a list of indices, each corresponding to the element in the input list 
        that should be at that position in the sorted list
        Example:
            input: [2,1,3]
            output: [1,0,2] (indexes corresponding to [1,2,3] in the input list)
        Rationale: This is done because this function is used for both Q1 and Q2 and Q2 has 
                   a need to remember the original word present in list1.
        :input: an unsorted list of non-negative integers of length N
        :output: a list of indices (of length N) with each index corresponding to the position 
                 of the element in the unsorted list that should be in the position of that 
                 index in the sorted list
        :time complexity: best and worst case is O(N+M) where N is the size of the input list 
                          and M is the value of the largest element in the input list
                          Calculation: O(N) + O(M) + O(N) + O(N+M) = O(N+M)
        :aux space complexity: O(M) since we need a count_array whose length is of the largest
                               element, M, in the input list;
        :space complexity: O(N+M) where N is the size of the input list and M is for the aux 
                           space (used for count_array)
    """
    if len(new_list) == 0:
        return new_list
    # find the maximum element 
    max_item = find_max(new_list)
    # initialise count_array
    count_array = [None] * (max_item+1)
    # create a new list of lists 
    for i in range(len(count_array)): # this loop runs in O(M) time
        count_array[i] = []
    # update count_array 
    for i in range(len(new_list)): # this loop runs in O(N) time
        count_array[new_list[i]].append(i)
    # update input array
    index = 0
    for lst in count_array: # this whole loop runs in O(M+N) time
        if len(lst) > 0:
            for i in range(len(lst)):
                new_list[index] = lst[i]
                index += 1
    return new_list

# helper function for Task 1
def radix_sort_int(new_list):
    """ This function takes as input an unsorted list of non-negative integers and sorts it by 
        applying counting_sort_index onto each column of digits in the elements of the input list
        and finally returns a list of elements from the input in sorted position
        :input: an unsorted list of non-negative intergers of length N
        :output: a sorted list of non-negative integers of length N
        :time complexity: best and worst case O(kN) where N is the length of the input list and k 
                          is the largest number of digits in a single element in the input list
                          Calculation: O(N) + O(k) + O(k) * O(N+N+N) = O(kN)
                          Counting sort runs in O(N) time (explained in Note)
        :aux space complexity: O(kN) as counting sort takes an input of size N, 
                               k times;
                               N is the length of the input list and k is the largest number of 
                               digits in a single element in the input list;
                               sorted_list, curr_column and new_list take O(N) space
        :space complexity: O(kN) since the length of the input list is N and the number of columns 
                           is k (maximum number of digits in a single element in the input list)
        Note: M (the base used to divide up columns for counting_sort_index) is a constant of base 10
    """
    if len(new_list) == 0:
        return new_list
    base = 10
    sorted_list = [0] * len(new_list)
    # finds the largest number of digits in a single element in the input list
    max_item = find_max(new_list)
    max_digits = 0
    if max_item == 0:
        max_digits = 1
    else:
        while max_item > 0: # this loop runs in O(k) time
            max_item = max_item//10
            max_digits += 1
    for exp in range(max_digits): # this loop runs in O(k) time
        curr_column = []
        for item in new_list: # this loop runs in O(N) time
            curr_digit = item // (base**exp) % base 
            curr_column.append(curr_digit)
        # sorted_list_index returns the index of the elements
        sorted_list_index = counting_sort_index(curr_column) # this loop runs in O(N) time
        # reassign all elements a new position in new_list
        index = 0
        for i in sorted_list_index: # this loop runs in O(N) time
            sorted_list[index] = new_list[i]
            index += 1  
        new_list = sorted_list[:]
    return sorted_list

# helper function for Task 1
def find_max(new_list):
    """ This function iterates through the input list and returns the maximum element
        of the list. If the list is empty, it returns None. However, the list is never
        empty as best_interval will not call this function if the length of its input
        list is 0
        :input: a list of integers of length N
        :output: the maximum element of the input list;
                 if the list is empty, the function returns None
        :time complexity: best and worst O(N) where N is the length of the input list
                          since we need to iterate through the whole list
        :aux space complexity: O(1) since we only keep updating max_item
        :space complexity: O(N) where N is the length of the input list
    """
    # pre-condition although input is never an empty list (reasoned above)
    if len(new_list) == 0:
        return None
    max_item = new_list[0]
    for item in new_list: 
        if item > max_item:
            max_item = item
    return max_item

# helper function for Task 2
def radix_sort_words(new_list):
    """ This function performs a radix sort on an unsorted list of strings and returns the 
        sorted list together with a list of indices where the elements in the indices list 
        indicate the position of the string (in the sorted list) in the original unsorted 
        list. This is done as we need to remember the original word in the input list using
        the indices
        Example: input: ["duck", "cow", "hen"]; output: [ ["cow", "duck", "hen"], [1,0,2] ]
        :input: an unsorted list of strings where the length of the list is N and
                the longest string in the list is of length M
        :output: a sorted list of strings of length N and a list of indices indicating 
                 the position of strings in the sorted list in the input list
        :time complexity: best and worst  O(NM) as counting sort needs to be performed for every 
                          letter up to the length of the longest string in the input
                          list
                          Calculation: O(N) + O(N) + O(M) * O(N+N+N) = O(NM)
        :aux space complexity: O(NM) as we need to call counting_sort_index M times 
                               (each counting_sort_index takes O(N) space);
                               sorted_list, sorted_list1, new_list, curr_column and 
                               prev_sorted_list1 takes O(N) space each
        :space complexity: O(NM) since we have an input list of length N and the number of 
                           columns is M (this is also the length of the longest string in the 
                           input list)
        Note: k (the base used to divide up elements) is not 
              included in the complexity as it is a constant
    """
    if len(new_list) == 0:
        return new_list
    # find the longest string in the list
    max_len = len(new_list[0])
    for strings in new_list: 
        if len(strings) > max_len:
            max_len = len(strings)
    # default value is the empty string so empty string can be sorted as well if present
    sorted_list = [""]*len(new_list)
    # store position of strings relative to original input list
    sorted_list1 = []
    prev_sorted_list1 = []
    for i in range(len(new_list)): # this loop runs in O(N) time
        sorted_list1.append(i)
        prev_sorted_list1.append(i)
    # loop from the rightmost alphabet because it has lowest priority in sorting
    for i in range(max_len-1, -1, -1): # this loop runs in O(M) time
        curr_column = []
        for item in new_list: # this loop runs in O(N) time
            if i < len(item):
                letter = item[i]
            else:
                letter = "`"
            curr_digit = ord(letter)-96
            curr_column.append(curr_digit)
        # sorted_list returns the index of the elements
        sorted_list_index = counting_sort_index(curr_column) # this loop runs in O(N) time
        index = 0
        for i in sorted_list_index: # this loop runs in O(N) time
            sorted_list[index] = new_list[i]
            sorted_list1[index] = prev_sorted_list1[i]
            index += 1
        prev_sorted_list1 = sorted_list1[:]
        # update new_list for next iteration
        new_list = sorted_list[:]
    return [sorted_list, sorted_list1]

# helper function for Task 2
def sort_word(word):
    """ This function takes as input a string and splits it into a list of letters, to_sort.
        The length of the list, to_sort, equals to the length of the word, M
        Thus, the maximum length of strings in the list is 1.
        Then, the alphabets in the list are sorted in lexicographic order using counting sort.
        :input: an unsorted string of length M
        :output: a sorted string of length M
        :time complexity: best and worst O(M) because the list to_sort is of length M (we need
                          to iterate through the whole list).
                          Calculation: O(M) + O(M) + O(M) = O(M)
                          Calling counting sort on a list whose elements and unique characters
                          are constants gives the counting sort a complexity of O(M) where M is 
                          the length of the list which is equal to the length of the input string
        :aux space complexity: O(M) as we need to convert letters to ASCII and store in to_sort
                               and back into a string of length M
        :space complexity: O(M) as input is of length M
    """
    if len(word) == 0:
        return word
    to_sort = []
    for letter in word: 
        to_sort.append(ord(letter)-96)
    # complexity of counting sort is O(M) as the number of unique characters is constant
    sorted_list_index = counting_sort_index(to_sort)
    index = 0
    for i in sorted_list_index: 
        to_sort[index] = word[i]
        index += 1  
    return "".join(to_sort)

# helper function for Task 2
def remove_duplicates(sorted_list):
    """ This functions takes in a sorted list of elements and returns a list of
        all the unique elements in the list in sorted order.
        :input: a sorted list of elements of length N
        :output: a sorted list of elements with only unique elements from the input
                 list
        :time complexity: best and worst O(N) where N is the length of the input list
                          since we will have to iterate through the whole list
        :aux space complexity: O(1) since we only update variable values 
                               (swapping is done in-place)
        :space complexity: O(N) as size of input list is N
    """
    i = 0
    j = 0
    last_index = 0
    while i < len(sorted_list)-1:
        if sorted_list[j] == sorted_list[i+1]:
            # move on
            i += 1
        else:
            # swap 
            last_index = j+1
            sorted_list[j+1], sorted_list[i+1] = sorted_list[i+1], sorted_list[j+1]
            i += 1
            j += 1
    return(sorted_list[:last_index+1])

list1 = ['bat', 'rats', 'god', 'dog', 'act', 'arts', 'star']
list2 = ['rats', 'dog', 'cat', 'arts', 'star']
#list1 = ["", ""]
#list2 = [""]
print(words_with_anagrams(list1, list2))
