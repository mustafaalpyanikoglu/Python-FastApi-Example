from fastapi import Header, HTTPException, status


async def get_token_header(x_token: str = Header("fake-super-secret-token")):
	if x_token != "fake-super-secret-token":
		raise HTTPException(
			status_code = status.HTTP_400_BAD_REQUEST,
			detail = "X-Token header Invalid"
		)


async def get_query_token(token: str = "jessica"):
	if token != "jessica":
		raise HTTPException(
			status_code = status.HTTP_400_BAD_REQUEST,
			detail = "Token header Invalid"
		)
