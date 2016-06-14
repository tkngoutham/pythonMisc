

pwkp_corpus='/home/kushwanth/PWKP_108016'
pwkp_complex='/home/kushwanth/PWKP_complex'
pwkp_simple='/home/kushwanth/PWKP_simple'

curr_pair=''
current_line=''
with open(pwkp_corpus,'r') as fp:
    total_content=fp.read()
    total_content=total_content.split('\n\n');
    print  len(total_content)
    for pair in total_content:
        #print pair
        curr_pair=pair.split('\n');
        #print curr_pair
        #print "----------------------------------"
        with open(pwkp_complex, "a") as complex:
            complex.write(curr_pair[0]+'\n')
            complex.close()
        with open(pwkp_simple, "a") as simple:
            len_curr_pair=len(curr_pair)
            for line in curr_pair[1:len_curr_pair]:
                current_line=current_line+' '+line
            simple.write(current_line+'\n')
            simple.close()
            current_line=''




