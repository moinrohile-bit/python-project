import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np

# ----------------------------------------------------
# 0. Setup Device (Optimized for Mac CPU/Apple Silicon)
# ----------------------------------------------------
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print(f"Using device: {device}")

# ----------------------------------------------------
# 2. Implement Data Augmentation & Loading
# ----------------------------------------------------
# Training augmentations to increase dataset variability
train_transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.RandomCrop(32, padding=4),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

# Validation transform (No augmentations, just normalization)
test_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

trainset = torchvision.datasets.CIFAR-10(root='./data', train=True, download=True, transform=train_transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=64, shuffle=True)

testset = torchvision.datasets.CIFAR-10(root='./data', train=False, download=True, transform=test_transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=64, shuffle=False)

classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

# ----------------------------------------------------
# 1 & 3. Enhanced Model Structure & Hyperparameters
# ----------------------------------------------------
class EnhancedCNN(nn.Module):
    def __init__(self):
        super(EnhancedCNN, self).__init__()
        # Convolutional layers with Batch Normalization
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        
        # Hyperparameter choice: LeakyReLU for better gradient flow
        self.leaky_relu = nn.LeakyReLU(0.1)
        self.pool = nn.MaxPool2d(2, 2)
        self.dropout = nn.Dropout(0.3)
        
        # Fully connected layers
        self.fc1 = nn.Linear(64 * 8 * 8, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.pool(self.leaky_relu(self.bn1(self.conv1(x))))
        x = self.pool(self.leaky_relu(self.bn2(self.conv2(x))))
        x = x.view(-1, 64 * 8 * 8)
        x = self.dropout(self.leaky_relu(self.fc1(x)))
        x = self.fc2(x)
        return x

model = EnhancedCNN().to(device)

# Hyperparameter Optimization: RMSprop Optimizer & CrossEntropy Loss
criterion = nn.CrossEntropyLoss()
optimizer = optim.RMSprop(model.parameters(), lr=0.001, alpha=0.99)

# ----------------------------------------------------
# Training Loop (Tracking Loss & Accuracy)
# ----------------------------------------------------
epochs = 5
history = {'loss': [], 'accuracy': []}

print("Starting training...")
for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    for i, data in enumerate(trainloader, 0):
        inputs, labels = data[0].to(device), data[1].to(device)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
        
    epoch_loss = running_loss / len(trainloader)
    epoch_acc = (correct / total) * 100
    history['loss'].append(epoch_loss)
    history['accuracy'].append(epoch_acc)
    print(f"Epoch {epoch+1}/{epochs} - Loss: {epoch_loss:.4f} - Accuracy: {epoch_acc:.2f}%")

print("Training finished.")

# ----------------------------------------------------
# 4. Visualize Performance and Predictions
# ----------------------------------------------------
# Plot Loss and Accuracy Curves
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history['loss'], label='Loss', color='red')
plt.title('Model Loss Performance')
plt.xlabel('Epochs')
plt.ylabel('Loss')

plt.subplot(1, 2, 2)
plt.plot(history['accuracy'], label='Accuracy', color='blue')
plt.title('Model Accuracy Performance')
plt.xlabel('Epochs')
plt.ylabel('Accuracy (%)')
plt.show()

# Visualize Test Sample Predictions
model.eval()
dataiter = iter(testloader)
images, labels = next(dataiter)

# Get predictions
outputs = model(images.to(device))
_, predicted = torch.max(outputs, 1)

# Unnormalize and plot helper function
def imshow(img):
    img = img / 2 + 0.5     # unnormalize
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))

# Show 4 test samples with true vs predicted labels
plt.figure(figsize=(10, 4))
for i in range(4):
    plt.subplot(1, 4, i+1)
    imshow(images[i])
    color = "green" if predicted[i] == labels[i] else "red"
    plt.title(f"True: {classes[labels[i]]}\nPred: {classes[predicted[i]]}", color=color)
    plt.axis('off')
plt.suptitle("Sample Model Predictions")
plt.show()
