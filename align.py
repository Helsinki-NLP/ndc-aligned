#! /usr/bin/env python3

import os, re, edlib

all_utterances, all_tokens = 0, 0

short = {
	"va": ["var"],
	"ha": ["har"],
	"he": ["har"],
	"me": ["med"],
	"de": ["det"],
	"å": ["og"],
	"hann": ["han"],
	"kann": ["kan"],
	"menn": ["men"],
	"mænn": ["men"],
	"vill": ["vil"],
	"komm": ["kom"],
	"somm": ["som"],
	"e": ["jeg", "er"],
	"eg": ["jeg"],
	"æ": ["jeg", "er"],
	"je": ["jeg"],
	"no": ["nå"],
	"atte": ["at"],
	"att": ["at"],
	"allt": ["alt"],
	"vett": ["vet"],
	"næi": ["nei"],
	"ætt": ["et"]
}

def tokenize(line):
	line = line.replace("dalsbygda_04gk_", "dalsbygda_04gk")	# fix some typos
	line = line.replace("trondheim_01um_", "trondheim_01um")
	line = line.replace("unknown_soldier", "unknown")
	tokens = line.strip().split(" ")
	tokens = [t for t in tokens if t != '' and t != '"']
	if tokens == []:
		return "", tokens
	
	speaker = ""
	if re.match(r'([\w_]+_\d\d(\w\w)?)', tokens[0]):
		speaker = tokens[0]
		tokens.pop(0)
	elif len(tokens[0]) == 2 or len(tokens[0]) == 3:
		speaker = tokens[0]
		if speaker == "jb":
			speaker = "jbj"
		tokens.pop(0)
	elif tokens[0] == "speaker#3" or tokens[0] == "speaker#4" or tokens[0] == "unknown":
		speaker = tokens[0]
		tokens.pop(0)
	else:
		print("  No speaker found")
		print("  ", tokens)
	return speaker, tokens


def align(orig_f, norm_f, out_f, fileid):
	global all_utterances, all_tokens
	out_f.write(f'<doc id="{fileid}">\n')
	norm_tokens = []
	nb_utterances, nb_tokens = 0, 0
	for line in orig_f:
		aligned = []
		non_verified = 0
		non_normalized = False
		orig_speaker, orig_tokens = tokenize(line)
		for t in orig_tokens:
			if norm_tokens == []:
				norm_speaker, norm_tokens = tokenize(norm_f.readline())
				if norm_tokens == []:
					print("  Normalization file ended early")
					print("  ", t)
					norm_tokens = [""]
					non_normalized = True
			
			if t == norm_tokens[0]:
				non_verified = 0
			elif len(t) > 4 and len(norm_tokens[0]) > 4:
				d = edlib.align(t, norm_tokens[0])
				if d['editDistance'] <= 0.5 * max(len(t), len(norm_tokens[0])):
					non_verified = 0
				else:
					non_verified += 1
			elif t in short:
				if norm_tokens[0] in short[t]:
					non_verified = 0
				else:
					non_verified += 1
			else:
				non_verified += 1
			
			aligned.append((t, norm_tokens[0]))
			norm_tokens.pop(0)

			if non_verified > 9:
				print("  Uncertain:")
				print("  ", " ".join([x[0] for x in aligned[-10:]]))
				print("  ", " ".join([x[1] for x in aligned[-10:]]))
			if orig_speaker != norm_speaker and norm_speaker != "":
				print("  Speaker mismatch:", orig_speaker, norm_speaker)
		
		if aligned != []:
			n = ' missing_norm="yes"' if non_normalized else ''
			out_f.write(f'<u id="{nb_utterances+1}" speaker="{orig_speaker}"{n}>\n')
			for orig, norm in aligned:
				out_f.write(f"{orig}\t{norm}\n")
			nb_utterances += 1
			nb_tokens += len(aligned)
			out_f.write('</u>\n')
	out_f.write('</doc>\n')
	print(f"  {nb_utterances} utterances, {nb_tokens} tokens")
	all_utterances += nb_utterances
	all_tokens += nb_tokens


if __name__ == "__main__":
	try:
		os.mkdir("aligned")
	except FileExistsError:
		pass

	filenames = os.listdir("ndc_phon_with_informant_codes/files/norwegian")
	for filename in filenames:
		print(filename)
		orig_f = open("ndc_phon_with_informant_codes/files/norwegian/" + filename, 'r')
		norm_f = open("ndc_with_informant_codes/files/norwegian/" + filename, 'r')
		out_f = open("aligned/" + filename.replace(".txt", ".vrt"), 'w')
		align(orig_f, norm_f, out_f, filename.replace(".txt", ""))
		orig_f.close()
		norm_f.close()
		out_f.close()
	
	print("Total:")
	print(f"  {all_utterances} utterances, {all_tokens} tokens")
