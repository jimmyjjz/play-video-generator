import torch
from diffusers import StableDiffusion3Pipeline, AutoPipelineForText2Image, DEISMultistepScheduler


def grab_image_prompts(sectioned_sequence:list)->list:
    p=[]
    for ss in sectioned_sequence:
        p.append(ss[0].split("-")[2])#+",professional photograph, realistic, award winning, dramatic, ultra-detailed, beautiful lighting, sharp focus"
    return p

def generate_images_sd(prompts:list)->None:
    #"stabilityai/stable-diffusion-2-1"
    #"stabilityai/stable-diffusion-3.5-large"
    pipe = StableDiffusion3Pipeline.from_pretrained("stabilityai/stable-diffusion-3.5-medium", torch_dtype=torch.bfloat16)
    pipe.enable_attention_slicing()
    pipe = pipe.to("cuda")
    print(prompts)
    results = pipe(
        prompts,
        #negative_prompt=["(deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, painting, drawing, illustration, anime, mutated hands and fingers:1.4), (inaccurate skin color: 1.5), text, error, zoom in on face, cropped, close up, too close, close photo, ugly, lazy eye, weird eye position, duplicate, (deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, disconnected limbs, mutation, mutated, ugly, disgusting, amputation, fused fingers, too many fingers, (worst quality, low quality, normal quality:2), gross clothing, unfashionable clothing, nipple over clothes, low detail"],
        num_inference_steps=25,
        guidance_scale=6,
        height=16,#304
        width=16,
        #algorithm_type="sde-dpmsolver++",
        #use_karras_sigmas=True
    )
    images = results.images
    for i, img in enumerate(images):
        #img.save(f"temp_images\\{prompts[i]}.png")
        img.save(f"temp_images\\{i}.png")

def generate_images_ani_single(prompt:str)->None:
    pipe = AutoPipelineForText2Image.from_pretrained('Lykon/AAM_XL_AnimeMix', torch_dtype=torch.float16, variant="fp16")
    pipe.scheduler = DEISMultistepScheduler.from_config(pipe.scheduler.config)
    pipe = pipe.to("cuda")
    image = pipe(prompt, num_inference_steps=25, width=512, height=512).images[0]
    image.save(f"temp_images\\{prompt}.png")

def generate_images_ani_multi(prompts:list)->None:
    pipe = AutoPipelineForText2Image.from_pretrained('Lykon/AAM_XL_AnimeMix', torch_dtype=torch.float16, variant="fp16")
    pipe.scheduler = DEISMultistepScheduler.from_config(pipe.scheduler.config)
    pipe = pipe.to("cuda")
    images = pipe(prompts, num_inference_steps=25, width=512, height=512).images
    for i,img in enumerate(images):
        img.save(f"temp_images\\{prompts[i]}.png")