
'''

3.2.22 EMR_EOF Example
This section provides an example of an EMR_EOF record (section 2.3.4.1).
000037E0: 0E 00 00 00 14 00 00 00
000037F0:00 00 00 00 10 00 00 00 14 00 00 00 

'''

def parse_hex_dump(hex_dump): # This parses an xxd -g 1 style hex dump and returns a "bytes" object which corresponds to that hexdump.
	ls = hex_dump.splitlines() # Each line.
	o = b"" # Init output.
	for l in ls:
		assert ":" in l
		l = l[l.index(":")+1:]
		bs = l.split(" ")
		print(bs)
		for b in bs:
			if not b: # Empty string? (This can be caused by spaces in the front and end)
				continue
			i = int(b, base=16)
			assert 0 <= i <= 255 # Should represent single byte
			o += bytes([i])
	return o



if __name__=="__main__":
	ret = parse_hex_dump("000037E0: 0E 00 00 00 14 00 00 00\n000037F0:00 00 00 00 10 00 00 00 14 00 00 00 ")
	print("ret: "+str(ret))
	assert ret == b"\x0E\x00\x00\x00\x14\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x14\x00\x00\x00"
	exit(0)
