import {ref} from "vue";

// 存储完整的响应内容
const accumulatedResponse = ref("");

// 发送请求并获取响应内容的函数
const getAnswer = async () => {
    try {
        // 向本地服务器发送 POST 请求，获取生成的数据
        const response = await fetch("http://localhost:11434/api/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                model: "gemma2:2b",
                prompt: "hello",
            }),
        });

        // 检查响应是否包含 body
        if (!response.body) {
            throw new Error("ReadableStream not supported in this environment.");
        }

        // 获取响应的流式读取器
        const reader = response.body.getReader();
        console.log(reader);
        const decoder = new TextDecoder("utf-8");
        let done = false;

        let incompleteChunk = ""; // 用于存储未完整解析的数据块

        // 循环读取响应数据，直到读取完成
        while (!done) {
            const {value, done: readerDone} = await reader.read();
            done = readerDone;

            if (value) {
                // 将数据块解码为字符串
                const chunk = decoder.decode(value, {stream: true});
                incompleteChunk += chunk;

                try {
                    // 按行分割数据，过滤出有效的 JSON 行
                    const parsedChunks = incompleteChunk.split("\n").filter(line => {
                        try {
                            JSON.parse(line);
                            return true;
                        } catch {
                            return false;
                        }
                    });

                    // console.log(parsedChunks);
                    // 解析每个有效的 JSON 数据块，并更新显示内容
                    for (let i = 0; i < parsedChunks.length; i++) {
                        const parsedChunk = JSON.parse(parsedChunks[i]);
                        // console.log(parsedChunks);
                        accumulatedResponse.value += parsedChunk.response;
                    }

                    // 重置未解析的部分
                    incompleteChunk = "";
                } catch (parseError) {
                    console.error("Failed to parse chunk: ", parseError);
                }
            }
        }

        console.log("Stream ended"); // 打印流结束的消息
    } catch (error) {
        console.error("Error: ", error); // 打印错误信息
    }
};
getAnswer()

