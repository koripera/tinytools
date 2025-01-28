import math

def move(point,angle,length):
	#現在地　角度　距離　から到達地点を求める
	x,y = point
	movex = math.cos(math.radians(angle))*length +x
	movey = math.sin(math.radians(angle))*length +y
	return movex, movey

def vec(angle,length):
	#角度　距離　からベクトルを求める
	x = math.cos(math.radians(angle))*length
	y = math.sin(math.radians(angle))*length
	return x,y

def Nvec(x,y):
	#単位ベクトルを得る
	l = math.sqrt(x**2+y**2)
	if l == 0:return None
	x = x/l
	y = y/l
	return x,y

def distance(A,B):
	#二点間の距離を求める
	Ax,Ay,Bx,By = A[0],A[1],B[0],B[1]	
	d = math.sqrt( (Ax-Bx)**2 + (Ay-By)**2)
	return d

def angle(A,B):
	#任意の点Aから、別の点Bへの角度を求める(度数で返す)
	Ax,Ay,Bx,By = A[0],A[1],B[0],B[1]	
	if Ax == Bx:
		if   Ay == By:#二点が同一
			return None
		elif Ay > By: #BがAの上にある
			return math.degrees( math.atan( math.inf ) )
		elif Ay < By: #BがAの下にある
			return math.degrees( math.atan( -math.inf ) )
	else:
		get = math.degrees( math.atan2( (By-Ay) , (Bx-Ax) ))
		return get

def tilt(A,B):
	#二点間の傾き
	Ax,Ay,Bx,By = A[0],A[1],B[0],B[1]
	# t=0 → x軸に平行/t=None → y軸に平行		
	if (Ax-Bx) == 0:t = None 
	else:           t = (Ay-By) / (Ax-Bx)
	return t

def X_pline(A1,A2,B1,B2):
	#二点を通るAの直線と,二点を通るBの直線の交点を返す
	At = get_tilt(A1,A2)
	Bt = get_tilt(B1,B2)
	return line_cross2(A1,At,B1,Bt)

def X_line(A,At,B,Bt):
	#1点を通る傾きAtのA直線と,1点を通る傾きBtのB直線の交点を返す
	Ax,Ay,Bx,By = A[0],A[1],B[0],B[1]

	if At == Bt:#平行線(解なし)
		x = None
		y = None

	elif At == None:#Aがy軸平行のとき
		x = Ax
		y = Bt*(x-Bx)+By

	elif Bt == None:#Bがy軸平行のとき
		x = Bx
		y = At*(x-Ax)+Ay

	else:#交差する
		x = (Ax*At - Bx*Bt +By -Ay) / (At-Bt)
		y = At*(x-Ax)+Ay

	return (x,y)

def colid_ll(A1,A2,B1,B2):
	#二点間のAの線分と,二点間のBの線分の当たり判定を返す(True or False)
	hit = False
	A_small_x, A_large_x = min(A1[0],A2[0]), max(A1[0],A2[0])
	B_small_x, B_large_x = min(B1[0],B2[0]), max(B1[0],B2[0])

	x , y = line_cross(A1,A2,B1,B2)
	
	if x != None:#直線で交点があれば、線分上の判定
		A_online = A_small_x <= x <= A_large_x
		B_online = B_small_x <= x <= B_large_x

		if A_online and B_online:
			hit = True

	return hit

def colid_lo(pt1,pt2,core,r,mode=""):
	return colid_ol(core,r,pt1,pt2,mode)

def colid_ol(core,r,pt1,pt2,mode=""):
	#coreを原点とする半径rの円と,
	#二点間の線分の当たり判定を返す(True or False)	

	#線分への垂線が交差するとき
	#	core-交点 < 半径 なら当たり

	#線分への垂線が交差しないとき
	#	近い端点 < 半径 なら当たり

	core_x , core_y = core
	pt1_x  , pt1_y  = pt1
	pt2_x  , pt2_y  = pt2	

	#判定用変数
	hit = False

	#線分のXの範囲をとる
	point_small_x = min(pt1[0],pt2[0])
	point_large_x = max(pt1[0],pt2[0])
	point_small_y = min(pt1[1],pt2[1])
	point_large_y = max(pt1[1],pt2[1])

	#二点を通る直線の傾き
	t = tilt(pt1,pt2)

	#円の垂線との交点を探す
	if t==0:
		cross_x ,cross_y= X_line( pt1 ,0, core, None)
	elif t==None:
		cross_x ,cross_y= X_line( pt1 ,None, core, 0)
	else:
		cross_x ,cross_y= X_line( pt1 ,t, core,(1/-t))
	
	online = False
	#交点があれば、線分上にあるかの判定
	if cross_x != None:
		online1 = point_small_x <= cross_x <= point_large_x
		online2 = point_small_y <= cross_y <= point_large_y
		if online1 and online2:
			online = True

	if online:
		hit = (core_x - cross_x)**2 + (core_y - cross_y)**2 < r**2

	if not online:
		temp = (core_x - pt1_x)**2 + (core_y - pt1_y)**2 < r**2
		temp2 = (core_x - pt2_x)**2 + (core_y - pt2_y)**2 < r**2
		if temp or temp2:
			hit = True

	if mode=="":
		return hit

	if mode=="n_vec":
		return ( Nvec( (core_x-cross_x),(core_y-cross_y) ) )

def colid_oo(A,Ar,B,Br):
	Ax,Ay,Bx,By = A[0],A[1],B[0],B[1]
	return (Ax-Bx)**2 + (Ay-By)**2 < (Ar+Br)**2


if __name__ == "__main__":
	pass

