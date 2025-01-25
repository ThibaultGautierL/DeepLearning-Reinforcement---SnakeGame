import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear_layer1 = nn.Linear(input_size, hidden_size)
        self.linear_layer2 = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        x = F.relu(self.linear_layer1(x))
        x = self.linear_layer2(x)
        return x
    
    def save(self, file_name='model.pth'):
        model_path = './model'
        if not os.path.exists(model_path):
            os.makedirs(model_path)
        file_name= os.path.join(model_path, file_name)
        torch.save(self.state_dict(), file_name)

class QTrainer: 
    def __init__(self, model, learning_rate, discount_rate):
        self.learning_rate = learning_rate
        self.model = model
        self.discount_rate = discount_rate
        self.optimizer = optim.Adam(model.parameters(), lr=self.learning_rate)
        self.criterion = nn.MSELoss()

    
    def train_step(self, state, action, reward, new_state, game_over):
        state = torch.tensor(state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.float)
        reward = torch.tensor(reward, dtype=torch.float)
        new_state = torch.tensor(new_state, dtype=torch.float)

        if len(state.shape) == 1: 
            state = torch.unsqueeze(state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            new_state = torch.unsqueeze(new_state, 0)
            game_over = (game_over, )
        
        prediction = self.model(state)

        target = prediction.clone()
        for idx in range(len(game_over)):
            Q_new =  reward[idx]
            if not game_over[idx]:
                Q_new = reward[idx] + self.discount_rate * torch.max(self.model(new_state[idx]))
            
            target[idx][torch.argmax(action).item()] = Q_new

        self.optimizer.zero_grad()
        loss = self.criterion(target, prediction)
        loss.backward()

        self.optimizer.step()


