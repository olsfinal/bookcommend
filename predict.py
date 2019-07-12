import CF
import readFile

def predicting(userData,bookData,input,output):
    with open(input,'rb') as inputfile,open(output,'w') as outputfile:
        lines=str(inputfile.read())
        lines = lines.replace(r'\r', '').split(r'\n')
        count=0
        outputfile.write('userid;bookid;p_score\n')
        for line in lines[1:len(lines) - 1]:
            item = line.split(";")
            user=item[0]
            book=item[1]
            try:
                # print(userSubset)
                Recommendations = CF.CFRating(user, book,userData,bookData)
                # if Recommendations!=0:
                print(user,book,Recommendations)
                outputfile.write(user+';'+book+';'+str(Recommendations)+'\n')
            except:
                outputfile.write(user + ';' + book + ';' + '0' + '\n')
            finally:
                count+=1
                print(count)
        print(count)

if __name__ == '__main__':
    users,books=readFile.getRating()
    predicting(users,books,'test_ratings.csv','prediction.csv')