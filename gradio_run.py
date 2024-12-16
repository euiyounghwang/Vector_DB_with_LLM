import Langchain.workflow.gradio.gradio_run as gr


# def inference(my_input):
#     my_output = my_input
#     # processing
#     return my_output


def greet(name):
    return "Hello " + name + "!"


def main():
    # demo = gr.Interface(
    #     inference, 
    #     inputs=["text"], 
    #     outputs=["text"]
    # )
    demo = gr.Interface(fn=greet, inputs="text", outputs="text")
    demo.launch()


if __name__ == '__main__':
    main()