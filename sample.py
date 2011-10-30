testinput = """i = 1;
s = 0;

 L1:

	b = i > 100;

	if b goto L2;
	s = s + i;
	i = i + 1;
	goto L1;

 L2:
	goto L1;
 L3:
	return s;"""

testinput = """i = 1;
s = 0;

 L1:

	b = i > 100;

	if b goto L3;
	s = s + i;
	i = i + 1;
	goto L1;

 L2:
	return s;
	goto L1;
 L3:
	return s;"""

testinput2 = """
a = 1;

L1:

a = a;

b = a > 0;
if b goto L1;

c = 2;
return b;

"""
testinput2 = """
a = 1 + 2;
b = a + 1;
a = b + 1;
a = 10 * 2;
a = a + 1;
L1:

a = a;

b = a < 0;
if b goto L1;

c = 2;
return c;

"""


