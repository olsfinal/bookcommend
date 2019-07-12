import CF
import readFile

def predicting(userData,bookData,input,output):
    with open(input,'rb') as inputfile,open(output,'w') as outputfile:
        lines=str(inputfile.read())
        lines = lines.replace(r'\r', '').split(r'\n')
        for line in lines[1:len(lines) - 1]:
            item = line.split(";")
            user=item[0]
            book=item[1]
            try:
                userSubset = CF.subset(bookData, userData,book)
                Recommendations = CF.CFRecommend(user, userSubset, n=1)
                print(user,book,Recommendations)
                outputfile.write(user+';'+book+';'+str(Recommendations)+'\n')
            except:
                outputfile.write(user + ';' + book + ';' + '0' + '\n')

if __name__ == '__main__':
    users,books=readFile.getRating()
    predicting(users,books,'test_ratings.csv','prediction.csv')