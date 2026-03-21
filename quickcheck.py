import transformers
import torch

print("Transformers:", transformers.__version__)


print(torch.__version__)
print(torch.cuda.is_available())
if torch.cuda.is_available():
	print(torch.cuda.get_device_name(0))

