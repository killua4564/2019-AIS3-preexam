### MaoHash
- 分成兩部分來看

- mao192部分
    - 自己實作的hash 沒啥太大問題
    - 關鍵地方可以看到他會先補0xb0在做0x00的padding
    - 最後留8bytes放原生len(s) 湊齊128的倍數
```
def mao192(s):
	A = 0x41495333
	B = 0x7b754669
	C = 0x6e645468
	D = 0x65456173
	E = 0x74657245
	F = 0x6767217D
	def G(X,Y,Z):
		return (X ^ (~Z | ~Y) ^ Z) & 0xFFFFFFFF
	def H(X,Y,Z):
		return (X ^ Y ^ Z & X) & 0xFFFFFFFF
	def I(X,Y,Z):
		return ((X & ~Z) | (~Z & Y)) & 0xFFFFFFFF
	def J(X,Y,Z):
		return ((X ^ ~Z) | (X & ~Y)) & 0xFFFFFFFF
	def K(X,Y,Z):
		return ((~X & Z) | (~X & Z ^ ~Y)) & 0xFFFFFFFF
	def L(X,Y,Z):
		return ((~X & Y ^ Z) | (X & Y)) & 0xFFFFFFFF
	def M(X,Y):
		return (X << Y | X >> (32 - Y)) & 0xFFFFFFFF
	X = [int((0xFFFFFFFE) * cos(i)) & 0xFFFFFFFF for i in range(256)]
	s_size = len(s)
	s += bytes([0xb0])
	if len(s) % 128 > 120:
		while len(s) % 128 != 0: s += bytes(1)
	while len(s) % 128 < 120: s += bytes(1)
	s += bytes.fromhex(hex(s_size * 8)[2:].rjust(16, '0'))
	for i, b in enumerate(s):
		k, l = int(b), i & 0x1f
		A = (B + M(A + G(B,C,D) + X[k], l)) & 0xFFFFFFFF
		B = (C + M(B + H(C,D,E) + X[k], l)) & 0xFFFFFFFF
		C = (D + M(C + I(D,E,F) + X[k], l)) & 0xFFFFFFFF
		D = (E + M(D + J(E,F,A) + X[k], l)) & 0xFFFFFFFF
		E = (F + M(E + K(F,A,B) + X[k], l)) & 0xFFFFFFFF
		F = (A + M(F + L(A,B,C) + X[k], l)) & 0xFFFFFFFF
	return ''.join(map(lambda x : hex(x)[2:].rjust(8, '0'), [A, F, C, B, D, E]))
```
- socket部分
    - admin有預設好的密碼 不可得知
    - 然後用admin登入會先有個亂數當作session
    - 之後生成`mac = hash(username&&password&&sessionID)`
    - 然後讓你輸入`mac&&*session&&cmd`
        - 只要`session in *session and cmd == "flag"`就可以拿到FLAG
    - 看到這裡就知道很明顯是考LEA了
```
USERS = {}
USERS[b'Admin'] = SECRET_PASSWORD
USERS[b'Guest'] = b'No FLAG'

def vertify(*stuff):
	return mao192(b'&&'.join(stuff)).encode()

class Task(socketserver.BaseRequestHandler):

    def recv(self):
        return self.request.recv(1024).strip()

    def send(self, msg):
        if type(msg) == str :
            msg = bytes([ord(m) for m in msg])
        self.request.sendall(msg)

    def run(self, username, password, session):
        while True :
            self.send('\nWhat do you want to do?\n')
            mac,*sess,cmd = self.recv().split(b'&&')
            if mac == vertify(username,password,*sess,cmd) and session in sess[0]:
                if cmd == b'flag':
                    if username == b'Admin':
                        print("Someone Get Flag!!")
                        self.send(FLAG)
                        return
                    else :
                        self.send('Permission denial\n')
                    break
                elif cmd == b'hint':
                    self.send(HINT)
                elif cmd == b'report':
                    self.send('Leave some message to maojui and kick his ass.\n')
                    print(username.decode() + ':',self.recv().decode())
                elif cmd == b'exit':
                    self.send('exit')
                    break
                else :
                    self.send('Unknown command.')
            else :
                self.send('Refused!\n')
                break
        self.send('See you next time .')

    def handle(self):
        try :
            self.send('Welcome to our system!\nPlease Input your username : ')
            username = self.recv()
            if b'&' in username :
                self.send('')
                raise ValueError
            try :
                password = USERS[username]
            except :
                self.send("Are you new here?\nLet's set a password : ")
                password = self.recv()
                USERS[username] = password
                self.send("Well done.\n\n")
            self.send(f'Hello {username.decode()} \n')
            session = bytes.hex(os.urandom(10)).encode()
            self.send(f'Here is your session ID: {session.decode()}\n')
            self.send(f'and your MAC(username&&password&&sessionID) : {vertify(username,password,session).decode()}\n')
            self.run(username,password,session)
        except:
            self.send("??????")
            self.request.close()

class ForkingServer(socketserver.ForkingTCPServer, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 10205
    print(HOST,PORT)
    server = ForkingServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
```
- 先將mao192做到能擴展
```
def hack_mao192(mac, s, start=128): # s = append_string
    A, F, C, B, D, E = [int(mac[i:i+8], 16) for i in range(0, len(mac), 8)]
    s_size = len(s)
    s += bytes([0xb0])
    if len(s) % 128 > 120:
        while len(s) % 128 != 0: s += bytes(1)
    while len(s) % 128 < 120: s += bytes(1)
    s += bytes.fromhex(hex((s_size + start) * 8)[2:].rjust(16, '0'))
    for index, byte in enumerate(s):
	k, l = int(byte), index & 0x1f
	A = (B + M(A + G(B,C,D) + X[k], l)) & 0xFFFFFFFF
	B = (C + M(B + H(C,D,E) + X[k], l)) & 0xFFFFFFFF
	C = (D + M(C + I(D,E,F) + X[k], l)) & 0xFFFFFFFF
	D = (E + M(D + J(E,F,A) + X[k], l)) & 0xFFFFFFFF
	E = (F + M(E + K(F,A,B) + X[k], l)) & 0xFFFFFFFF
	F = (A + M(F + L(A,B,C) + X[k], l)) & 0xFFFFFFFF
    return (''.join(map(lambda x : hex(x)[2:].rjust(8, '0'), [A, F, C, B, D, E]))).encode()
```
- 我們拿到的mac是由`username&&password&&session`做hash得到的 除了password不知道長度之外 剩下的總和為29
- 因為長度不到120(除非`len(password) > 90`)所以mao192只會有一個block(main loop執行一次)
- 當輸入`username&&password&&session`的時候真正進入main loop的是`username&&password&&session+padding+length`
    - `padding = \xb0 + \x00 * (120 - length - 1)`
- 因為在輸入cmd的時候有個特性`session in *session`這邊可以讓`*session = [padding, session]` 這樣cmd就會順利被執行
- 最後只要讓`&&session&&cmd`用一開始拿到的mac接下去算hash就可以拿到新的而且正確的mac讓我們去傳送
- 實驗:
```
username = b"Admin"
password = b"secret_password"  # Assume
session = b"48bb668c85ea50cfc1f7"
mac = vertify(username, password, session)

cmd = b"flag"
length = len(username) + 2 + len(password) + 2 + len(session)
padding = session + b"\xb0" + b"\x00" * (120-length-1) + bytes.fromhex(hex(length * 8)[2:].rjust(16, '0'))

real_mac = vertify(username, password, padding, session, cmd)
hack_mac = hack_mao192(mac, b"&&" + session + b"&&" + cmd)

real_mac == hack_mac
>>> True
```
- 之後只要用個for去猜整體的長度就好了
```
from pwn import *
for length in range(29, 100):  # length = 93
	conn = remote("maojui.me", "11111")
	conn.recvuntil(" : ")
	conn.sendline("Admin")
	conn.recvuntil(": ")
	session = conn.recvuntil("\n").strip(b"\n")
	conn.recvuntil(" : ")
	mac = conn.recvuntil("\n").strip(b"\n")
	conn.recvuntil("?\n")
    
	cmd = b"flag"
	padding = session + b"\xb0" + b"\x00" * (120-length-1) + bytes.fromhex(hex(length * 8)[2:].rjust(16, '0'))
	mac = hack_mao192(mac, b"&&" + session + b"&&" + cmd)
    
	conn.sendline(b"&&".join([mac, padding, session, cmd]))
	print(length, conn.recv())
	conn.close()
```
- flag: `AIS3{imP13M3NT_Lea_I5_N0T_Soooo_HARD_right_xdddd}`