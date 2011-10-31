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

testinput3 = """

 i = 1;
 s = 0;
 b = i > 100;
 L1:
 b = i > 100;
 if b goto L2;
 s = s + i;
 i = i + 1;
 goto L1;
 L2:
 return s;
 a = 3;
 if a goto L3;
 L3:
 if a goto L4;
 a = a - 1;
 goto L3;
 L4:
 goto L2;
"""

testinput10 = """
a = 1 + 2;
b = a + 1;
a = b + 1;
a = 10 * 2;
a = a + 1;
L1:

a = a;
goto L2;
b = a < 0;
if b goto L2;

c = 2;
return c;
L2:
	return a;
	goto L1;
"""

testinput4 = """
a = 1 + 2;
b = a + 1;
a = b + 1;
a = 10 * 2;
a = a + 1;
L1:

a = a;
goto L2;
b = a < 0;
if b goto L1;

c = 2;
return c;
L2:
	if b goto L1;
"""
testinput5 = """
a = 1 + 2;
b = a + 1;
a = b + 1;
a = 10 * 2;
a = a + 1;
L1:

a = a;
goto L2;
b = a < 0;
if b goto L1;

c = 2;
goto L2;
L2:
	if b goto L1;
"""

testinput11 = """
c = 2;
L1:

c = c + 1;
b = c < 100;

if b goto L1;
a = 1;
b = a > 0;
if b goto L2;

return c;
L2:

return a;

"""
