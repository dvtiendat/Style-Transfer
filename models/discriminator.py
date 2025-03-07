import torch 
import torch.nn as nn
import torch.nn.functional as F

class BasicBlock(nn.Module):
    '''
    Convolutional block for discriminator
    '''
    def __init__(self, in_channels, out_channels, stride):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 4, stride, 1, bias=True, padding_mode='reflect'),
            nn.InstanceNorm2d(out_channels),
            nn.LeakyReLU(0.2)
        )

    def forward(self, x):
        return self.conv(x)

class Discriminator(nn.Module):
    '''
    Discriminator based on PatchGAN architecture, with each layer 
    with size of features = [64, 128, 256, 512]
    '''
    def __init__(self, in_channels=3, features=[64, 128, 256, 512]):
        super().__init__()
        self.init = nn.Sequential(
            nn.Conv2d(in_channels, features[0], kernel_size=4, stride=2, padding=1, padding_mode='reflect'),
            nn.LeakyReLU(0.2)
        )

        layers = []
        in_channels = features[0]
        for feature in features[1:]:
            layers.append(BasicBlock(in_channels, feature, stride=1 if feature==features[-1] else 2))
            in_channels = feature
        layers.append(nn.Conv2d(in_channels, 1, 4, 1, 1, padding_mode='reflect'))
        self.model = nn.Sequential(*layers)

    def forward(self, x):
        x = self.init(x)
        return torch.sigmoid(self.model(x))
