import asyncio

async def handle_client(reader, writer):
    print("클라이언트 연결됨")
    writer.write("1.인물등록\n2.게임시작\n3.프로그램 종료\n".encode())
    await writer.drain()

    while True:
        data = await reader.read(100)
        message = data.decode()
        print(f"클라이언트로부터 받은 데이터: {message}")

        if message == '3':
            print("클라이언트 연결 종료")
            break

        response = input("클라이언트에게 보낼 메시지를 입력하세요: ")
        writer.write(response.encode())
        await writer.drain()

async def main():
    server = await asyncio.start_server(
        handle_client, '192.0.0.1', 12345)

    addr = server.sockets[0].getsockname()
    print(f'서버가 {addr} 에서 실행 중...')

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
