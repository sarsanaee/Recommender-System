class SlopeOne(object):
    def __init__(self):
        self.diffs = {}
        self.freqs = {}

    def predict(self, userprefs):
        preds, freqs = {}, {}
        for item, rating in userprefs.iteritems():
            for diffitem, diffratings in self.diffs.iteritems():
                try:
                    freq = self.freqs[diffitem][item]
                except KeyError:
                    continue
                preds.setdefault(diffitem, 0.0)
                freqs.setdefault(diffitem, 0)
                preds[diffitem] += freq * (diffratings[item] + rating)
                freqs[diffitem] += freq
        return dict([(item, value / freqs[item])
                     for item, value in preds.iteritems()
                     if item not in userprefs and freqs[item] > 0])

    def update(self, userdata):
        for ratings in userdata.itervalues():
            for item1, rating1 in ratings.iteritems():
                self.freqs.setdefault(item1, {})
                self.diffs.setdefault(item1, {})
                for item2, rating2 in ratings.iteritems():
                    self.freqs[item1].setdefault(item2, 0)
                    self.diffs[item1].setdefault(item2, 0.0)
                    self.freqs[item1][item2] += 1
                    self.diffs[item1][item2] += rating1 - rating2
        for item1, ratings in self.diffs.iteritems():
            for item2 in ratings:
                ratings[item2] /= self.freqs[item1][item2]



def find_difference(result,data, user):
    max_error = 0
    error_list = []
    for i in result.keys():
        try:
            max_error = max_error + data[user][i] - result[i]
            error_list.append(abs(data[user][i] - result[i]))
        except:
            max_error = max_error
    #print "fuck"
    #print (max_error)
    return max_error, error_list


if __name__ == '__main__':
    '''
    userdata = dict(
        alice=dict(squid=1.0,
                   cuttlefish=0.5,
                   octopus=0.2),
        bob=dict(squid=1.0,
                 octopus=0.5,
                 nautilus=0.2),
        carole=dict(squid=0.2,
                    octopus=1.0,
                    cuttlefish=0.4,
                    nautilus=0.4),
        dave=dict(cuttlefish=0.9,
                  octopus=0.4,
                  nautilus=0.5),
        )
    '''

    s = SlopeOne()
    errors = []

    data = {}
    with open('/home/alireza/Desktop/ml100k/u1.base', 'r') as fp:
        for line in fp:
            temp = line.split()
            if(data.has_key(temp[0])):
                data[temp[0]][temp[1]] = int(temp[2])
            else:
                dictionary = {}
                dictionary[temp[1]] = int(temp[2])    
                data[temp[0]] = dictionary
            
    
    s.update(data)
    
    
    
    ## 
    ###  Prediction :)))))
    

    pre_user = '1'
    dictionary = {}
    with open('/home/alireza/Desktop/ml100k/u1.test', 'r') as fp:
        for line in fp:
            temp = line.split()
            if(pre_user != temp[0]):
                errors.append(find_difference(s.predict(dictionary), data, pre_user))
                dictionary = {}
                dictionary[temp[1]] = int(temp[2])
                
            else:
                dictionary[temp[1]] = int(temp[2])
            
            pre_user = temp[0]
            
    total_errors = 0
    for i in errors:
        total_errors = total_errors + i[0]/len(i[1])
    print total_errors/len(errors)
