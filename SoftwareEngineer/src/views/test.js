import {ref, nextTick, computed, onBeforeMount} from 'vue';
let accumulatedChunk =ref("")
const getAnswer = async () => {
    // console.log("已发送", newMessage.value);
    try {
        // 向本地服务器发送 POST 请求，获取生成的数据
        const response = await fetch("http://127.0.0.1:8000/ai/internet/back", {
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
        //response.body 是一个流式的接口，通过 getReader() 来逐步读取到服务器返回的数据。在流结束之前，数据是分段到达的，并不是一次性获取到完整的响应
        //reader类似于一个生成器
        const reader = response.body.getReader();

        //创造解码器对象
        const decoder = new TextDecoder("utf-8");
        //判断是否已经流式返回完
        let done = false;

        let incompleteChunk = ""; // 用于存储未完整解析的数据块


        // 循环读取响应数据，直到读取完成
        while (!done) {
            const {value, done: readerDone} = await reader.read();
            done = readerDone;

            if (value) {
                // 将二进制数据块解码为字符串
                const chunk = decoder.decode(value, {stream: true});
                console.log(chunk);
                //存储字符串
                incompleteChunk += chunk;


                try {
                    //解析字符串生成的是单个返回的JSON对象
                    console.log(incompleteChunk)
                    const parsedChunk = JSON.parse(incompleteChunk);

                    // 将解析后的内容追加到 messages 中
                    accumulatedChunk.value += parsedChunk.response;


                    // 重置未解析的部分
                    incompleteChunk = "";
                } catch (parseError) {
                    console.error("JSON解析失败: ", parseError);
                    incompleteChunk = "";
                }
            }
        }

        console.log(accumulatedChunk.value)
        console.log("流结束"); // 打印流结束的消息
    } catch (error) {
        console.error("错误: ", error); // 打印错误信息
    }
};
getAnswer()
