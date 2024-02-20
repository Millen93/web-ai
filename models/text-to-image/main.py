from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse
from pydantic import BaseModel
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler, AutoencoderKL
import torch
import random
import uvicorn

pipe = DiffusionPipeline.from_pretrained(
    "prompthero/openjourney",
    torch_dtype=torch.float32,
    safety_checker = None
)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe.vae = AutoencoderKL.from_pretrained("stabilityai/sd-vae-ft-mse", torch_dtype=torch.float32)

num_steps = 20
num_variations = 1
prompt_guidance = 9
dimensions = (400, 600)  # (width, height) tuple
random_seeds = [random.randint(0, 65000) for _ in range(num_variations)]

app = FastAPI(title="Text To Image Model")


class Prompt(BaseModel):
    prompt: str


@app.post("/")
async def generate_image(prompt: Prompt):
    images = pipe(prompt=num_variations * [prompt.prompt],
                  num_inference_steps=num_steps,
                  guidance_scale=prompt_guidance,
                  height=dimensions[0],
                  width=dimensions[1],
                  generator=[torch.Generator().manual_seed(i) for i in random_seeds]).images
    images[0].save("./test0.png")
    return FileResponse("./test0.png")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=7000,
        log_level="debug",
        reload=True,
    )
