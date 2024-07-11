from footer import get_footer
import random
import wikipedia

def celebritytrivia_page(request):
    outtext = ""
    outtext = "<html><body><center>"
    outtext += "<h2>Celebrity Trivia</h2>"
    outtext += "Clues are given about a celebrity from their Wikipedia page and you have to guess the celebrity.<br><br><hr>"
    celebname = ''
    origname = ''
    if 'guess' in request.form:
        guess = request.form['guess']
        celebname = request.form['answer']
        myfile = open('/home/jimmyrustles/mysite/celeb_images.txt','r')
        lines = myfile.readlines()
        celeb_image_url = ''
        myfile.close()
        for line in lines:
            line = line.replace("\n","")
            line_celeb = line.split("|")[0]
            line_url = line.split("|")[1]
            if line_celeb.lower() == celebname.lower():
                celeb_image_url = line_url
                break
        if guess.lower() == celebname.lower():
            outtext += "<font color='#00BB00'>Correct! The answer was " + celebname + "</font><br><br>"
            if celeb_image_url != '':
                outtext += '<img src="' + celeb_image_url + ' height="250"><br><br>'
            outtext += "<a href='/celebrity_trivia'>Play a New Game</a>"
            outtext += "</center></body></html>"
            return outtext
        else:
            outtext += "<font color='#BB0000'>Incorrect! The answer was " + celebname + "</font><br><br>"
            if celeb_image_url != '':
                outtext += '<img src="' + celeb_image_url + '" height="250"><br><br>'
            outtext += "<a href='/celebrity_trivia'>Play a New Game</a>"
            outtext += "</center></body></html>"
            return outtext
    if 'answer' in request.form:
        celebname = request.form['answer']
        origname = celebname
    else:
        with open('/home/jimmyrustles/mysite/celebs.txt', 'r') as ff:
            celebrities = [line.split('\n')[0] for line in ff.readlines()]
        celebname = random.choice(celebrities)
        origname = celebname
    page = ''
    while page == '':
        try:
            page = wikipedia.page(origname, auto_suggest=False)
        except:
            with open('/home/jimmyrustles/mysite/celebs.txt', 'r') as ff:
                celebrities = [line.split('\n')[0] for line in ff.readlines()]
            celebname = random.choice(celebrities)
            origname = celebname
    lines = page.content.split("\n")

    clues, potential_clues = [], []
    censored_names = [name for name in origname.split() if len(name) > 1]
    for i, line in enumerate(lines):
        line = line.replace("Dr. ", "Dr ").replace("Mr. ", "Mr ").replace("Gen. ", "Gen ").replace("No. ", "No ").replace("U.S. ", "US ")
        sentences = line.split(". ")

        matches = [
            "== Awards", "== Legacy and awards", "== Titles",  "== External", "== Filmography",
            "== Discography", "== See also", "== Electoral history", "== Authored books", "== References"
        ]
        if any(match in line for match in matches):
            break

        if "==" in sentences[0]: continue
        if sentences[0] == "": continue
       # if 1 < len(sentences[0]) <= 10:
        #    sentences[0] += "." + sentences[1]

        if i == 0:
            if len(sentences[0]) <= 10:
                sentences[0] += "." + sentences[1]
            name = sentences[0].split(" is ")[0]
            name = name.split(" was ")[0]
            name = name.split(" (born")[0]
            for namepiece in name.split(" "):
                censored_names.append(namepiece)
            censoredline = sentences[0]
            for word in censored_names:
                censoredline = censoredline.replace(word, "____")
            line = censoredline + "."
            outtext += "" + line + "<br><br>"
            continue

        censored_names = [name for name in censored_names if len(name) > 1]
        # censor celebrity's name
        censoredline = sentences[0]
        for word in censored_names:
            censoredline = censoredline.replace(word, "____")
        line = censoredline + "."

        potential_clues.append(line)

    for j, clue in enumerate(potential_clues):
        if len(clue) <= 7:
            potential_clues.pop(j)

    for i in range(5):
        if len(potential_clues) == 0: break
        randnum = random.randint(0, len(potential_clues) - 1)
        clue = potential_clues[randnum]
        potential_clues.pop(randnum)
        clues.append(clue)
    for i, clue in enumerate(clues, start=1):
        outtext += "Clue " + str(i) + ": " + clue + "<br><br>"
    outtext += "<form method='POST'><input type=\"hidden\" name=\"answer\" value=\"" + origname + "\"><input type=\"submit\" value=\"More Clues\"></form>"
    outtext += "<form method='POST'><input type='hidden' name='answer' value='" + origname + "'><input type='text' name='guess' value=''><input type='submit' value='Guess'></form>"
    outtext += "<a href='/celebrity_trivia'>Play a New Game</a>"
    outtext += get_footer()
    outtext += "</center></body></html>"
    return outtext