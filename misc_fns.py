
#reading entire data from a file
def _read_words(filename):
  with gfile.GFile(filename, "r") as f:
    #returning list of words with '\n' as "<eos>"
    return f.read().replace("\n", "<eos>").split()
    
def _build_vocab(filename):
  data = _read_words(filename)
  #data example ['blue', 'red', 'blue', 'yellow', 'blue', 'red']
  
  counter = collections.Counter(data)
  #Counter({'blue': 3, 'red': 2, 'yellow': 1})
  
  count_pairs = sorted(counter.items(), key=lambda x: -x[1])
  # sorted with x:-x[1] sorts counter in decreaing order according to col 1 ie no of times each word occurs
  #count_pairs : [('blue', 3), ('red', 2), ('yellow', 1)] 
  
  words, _ = list(zip(*count_pairs))
  #zip(*count_pairs) zips words and counts as separate lists into a single combined list
  # words will have only words in descending sorted order
  
  word_to_id = dict(zip(words, range(len(words))))
  #here words are assigned 0 to highly repeated words 1 to second highest repeated word and so on......
  # and finally least occured word has len(words)-1

  return word_to_id
  
  
