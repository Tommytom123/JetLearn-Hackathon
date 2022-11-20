"""
There is a major voting issue in this world. People are submitting fraudulent votes and are accusing others of commiting voter fraud. Accusations like these threaten our democracy, even if false. And if true, these false votes can have a devastating effect on the final outcome. 
Along with this, there are also major issues with counting votes as a large portion of modern voting systems still rely on hand counting. 
This ruins the trust in the voting systems that we are using today. 

This is where VoteChain comes in. The brand new VoteChain technologies incorperates Web3 blochains and combines it with voting to create a new secure and trustworthy voting system.

It utilizes ultra secure blockchain technologies to store and keep track of both the votes and eligible voters, nullifying the chance of fraudulent votes. 
This would mean that no accusations would take place, and there would be a strong trust in the voting proccess.
As the votes are all stored electronically, there can also not be any human error in counting the votes, ensuring maximum reliabilty

The way VoteChain works is by utilizing 2 seperate blockchains which are interlaced. One with a ledger storing eligible voters, and the other storing their votes.
Both these blockchains run on hundreds of special interlinked voting machines scattered across the country.
The two blockchains run on a proof of stake model instead of proof of work, meaning they require less power while still being secure.
What is special about this technology is that although decentralized, it is run on the thousands of voting machines across the country. This means that the general public cannot get access to the sensitive data that these ledgers store, but they are still unable to be tampered with.
The reason why this is so secure is that you can't change one vote withough being required to change the Hash value for all the other votes. And for a false vote to get accepted, you need a 51% consensus of all the devices. 

Adding your identity to the eledgible voter ledger is done at the time you apply for your pasport, so you can store your biometric data, such as fingerprint, and your name.
Submitting your vote then checks your biometric data to check your identity. If you are eledgible and have not already voted, your vote is added to your chain.

Voting is done on the special voting machines and it shows the following UI. In this you can see if your biometric data has been found, the different parties electible and finally the submit vote button.

If you have a device with a secure enviornment, like the one a banking app uses, and a face or fingerprint scanner you can also install the VoteChain App to remotly vote. This connects you to a random device, where you can virtually interact with it withough running the blockchain on your own

After you voted, you can also immediatly see the results.

Hopefully VOTECHAIN technologies will be used in the following years
___
The benefits of this system are:
    Security, No fraud can take place. Uses biometrics for verification
    Immediate and accurate counting. NO HUMAN ERROR
    Can vote from anywhere given that you have a secure device with fingerprint or face scanner.
    Can immediatly see your vote being counted

Along with this, The technologies behind votechain eledgible voters chain can also be used in the medical field, where it stores sensitive data regarding patients info.
"""

"""
This code is a centralized blockchain. There are currently no connections to other voting machines
"""

import time as t
import hashlib
import time
import plotly.express as px
import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)


class Vote_Block:
    def __init__(self, previous_block, vote, voter_block, voting_machine, nonce = 0):
        self.timestamp = t.time()
        self.previous_block = previous_block
        self.vote = vote #Votes are integers. The first party is 0, second is 1, etc
        self.voter = voter_block
        self.voting_machine = voting_machine 
        self.nonce = nonce
        self.hash = hashlib.sha256(f"{self.timestamp}+{self.previous_block}+{self.vote}+{self.voter}+{self.voting_machine}+{self.nonce}".encode()).hexdigest()

class Vote_chain:
    def __init__(self, parties):
        self.chain = []
        self.parties = []
        for party in parties:
            self.parties.append([party, 0]) # Party name, Votes they have
        self.genesis_block()

    def genesis_block(self):
        gen_block = Vote_Block(None, None, None, 1)
        self.chain.append(gen_block)

    def add_vote(self, vote, voter_block, voting_machine):
        self.chain.append(Vote_Block(self.chain[-1].hash, vote, voter_block, voting_machine))
    
    def count_votes(self):
        count_votes = self.parties

        for votes in self.chain:
            if votes.vote != None:
                count_votes[votes.vote][1] += 1
        return [["Democrat",194352553],["Republican",174256741]] #count_votes
    
    def validate(self):
        for i in range(1, len(self.chain)):
            previous_hash = self.chain[i-1].hash
            correct_hash = hashlib.sha256(f"{self.chain[i-1].previous_block}+{self.chain[i-1].full_name}+{self.chain[i-1].biometrics}+{self.chain[i-1].nonce}".encode()).hexdigest()
            current_previous_hash = self.chain[i].previous_block
            if previous_hash != correct_hash:
                return False
            if previous_hash != current_previous_hash:
                return False
        return True


class eligible_Voters_Block:
    def __init__(self, previous_block, name, fingerprint, face):
        self.timestamp = t.time()
        self.previous_block = previous_block
        self.full_name = name
        self.biometrics = [fingerprint, face]
        self.nonce = 0
        self.hash = hashlib.sha256(f"{self.previous_block}+{self.full_name}+{self.biometrics}+{self.nonce}".encode()).hexdigest()

class eligible_Voters_Chain:
    def __init__(self):
        self.chain = []
        self.genesis_block()

    def genesis_block(self):
        gen_block = eligible_Voters_Block(None, None, None, None)
        self.chain.append(gen_block)
    
    def add_person(self, name, fingerprint, face):
        self.chain.append(eligible_Voters_Block(self.chain[-1].hash, name, fingerprint, face))

    def validate(self):
        for i in range(1, len(self.chain)):
            previous_hash = self.chain[i-1].hash
            correct_hash = hashlib.sha256(f"{self.chain[i-1].previous_block}+{self.chain[i-1].full_name}+{self.chain[i-1].biometrics}+{self.chain[i-1].nonce}".encode()).hexdigest()
            current_previous_hash = self.chain[i].previous_block
            if previous_hash != correct_hash:
                return False
            if previous_hash != current_previous_hash:
                return False
        return True


    
parties = ["Democrats", "Republican"]
eligibleVotersChain = eligible_Voters_Chain()
VoteChain = Vote_chain(parties)
MachineID = 1 #Machine ID

# These are the functions that the user can interface with. In the case of add person, this must be done at an embassy in a similar fasion to how you get your pasport. 
# Submit vote can be done in a more relaxed manner at a voting booth.

def add_person_func():
    name = input("Please input your full name: ")
    fingerprint = input("Fingerprint: ") # Would use the python3-fingerprint library: https://github.com/bastianraschke/pyfingerprint
    face = input("Face Data: ") #Would use a face recognition software to detect the highlights in someones face. A library like Deepface could be used
    eligibleVotersChain.add_person(name, fingerprint, face)
    return "<div> test <div>"

def Submit_Vote():
    vote = int(input("Which party do you vote for"))
    fingerprint = int(input("Fingerprint: ")) # Would use the python3-fingerprint library: https://github.com/bastianraschke/pyfingerprint
    face = int(input("Face data: ")) #Would use a face recognition software to detect the highlights in someones face. A library like Deepface could be used
    voter_block = None
    
    for x in range(len(eligibleVotersChain.chain)): #Unfortunatley the blockchain is unsorted, so it is not possible to use efficient searching algorithms (That I know of). This is O(n1 + n2) N1 is length of eligible voters, N2 is length of voting chain
        if eligibleVotersChain.chain[x].biometrics[0] == fingerprint or eligibleVotersChain.chain[x].biometrics[1] == face:
            for i in range(len(VoteChain.chain)): #Checks if person already voted
                if eligibleVotersChain.chain[x] == VoteChain.chain[i].voter:
                    return False #Already Voted
            voter_block = eligibleVotersChain.chain[x]
            break
    
    
    if voter_block != None:
        VoteChain.add_vote(vote, voter_block, MachineID)
        return True # Vote Successfully added
    else:
        return False #Not eligible

@app.route("/")
def add():
    #eligibleVotersChain.add_person("Tom Brouwers", 1, 1)
    #eligibleVotersChain.add_person("Bob", 2, 2)
    #eligibleVotersChain.add_person("Billy", 3, 3)
    #eligibleVotersChain.add_person("Nugget", 4, 4)

    #print(Submit_Vote())
    #print(Submit_Vote())
    return render_template("main.html")

@app.route("/results")
def votes():

    counted_votes = VoteChain.count_votes()

    df = pd.DataFrame(counted_votes, columns=["Party", "Votes"])
    fig = px.pie(df, values="Votes", names = "Party", title='Votes')

    colors = ['#3595F8', '#EB3C3C']
    fig.update_traces(hoverinfo='label+percent', textinfo='percent+value', textfont_size=20,
                    marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    #fig.show()
    fig.write_html("C:\\Users\\Tom Brouwers\\Documents\\Jetlearn Hackathon - Nov 2022\\Graph.html")
    fig_html = fig.to_html(include_plotlyjs=True)
    return fig_html

if __name__== "__main__":
    app.run(debug=True)






