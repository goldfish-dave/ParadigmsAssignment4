testinput = """i = 1;
s = 0;

 L1:

	b = i > 100;

	if b goto L2;
	s = s + i;
	i = i + 1;
	goto L1;

 L2:
	return s;"""
