
%% Loading data for coursework1-a
data = load('cw1a.mat');
% train data
x = data.x;
y = data.y;
% test input data
xs = linspace(-3, 3, 61)';

%% Specify the mean, covariance and likelihood functions
meanfunc = [];              % empty: don't use a mean function
covfunc = @covSEiso;        % Squared Exponental covariance function
likfunc = @likGauss;        % Gaussian likelihood

% Init the hyperparameter struct
%   mean function is empty => no hyperparams needed
%   cov function has [ln(lengthscale), ln(sigma)] as hyperparams
%   likelihood function has [ln(sigma)] as hyperparam
hyp = struct('mean', [], 'cov', [-1 0], 'lik', 0);

%% Training
% Set hyperparameters by optimizing the (log) marginal likelihood
hyp2 = minimize(hyp, @gp, -100, @infGaussLik, meanfunc, covfunc, likfunc, x, y);

%% Prediction
% Make predictions using these hyperparameters
[mu, s2] = gp(hyp2, @infGaussLik, meanfunc, covfunc, likfunc, x, y, xs);

%% Plotting results
% Plot the predictive mean at the test points together with the
% predictive 95% confidence bounds and the training data
f = [mu+2*sqrt(s2); flip(mu-2*sqrt(s2),1)];
fill([xs; flip(xs,1)], f, [7 7 7]/8)
hold on;
% Plotting predictive distribution (predictive mean and confidence bounds)
plot(xs, mu);
% Plotting training data points
plot(x, y, '+')

xlabel("x");
ylabel("y");
title("Plot of the training data and the predictive mean at the test points together with the predictive 95% confidence bounds");


