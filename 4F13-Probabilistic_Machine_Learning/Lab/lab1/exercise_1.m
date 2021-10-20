
% Loading data for coursework1-a
data = load('cw1a.mat');
x = data.x;
y = data.y;
xs = linspace(-3, 3, 61)';

% We need specify the mean, covariance and likelihood functions
meanfunc = [];              % empty: don't use a mean function
covfunc = @covSEiso;        % Squared Exponental covariance function
likfunc = @likGauss;        % Gaussian likelihood

% Init the hyperparameter struct
hyp = struct('mean', [], 'cov', [-1 0], 'lik', 0);

% Set hyperparameters by optimizing the (log) marginal likelihood
hyp2 = minimize(hyp, @gp, -100, @infGaussLik, meanfunc, covfunc, likfunc, x, y);

% Make predictions using these hyperparameters
[mu s2] = gp(hyp2, @infGaussLik, meanfunc, covfunc, likfunc, x, y, xs);

% Plot the predictive mean at the test points together with the
% predictive 95% confidence bounds and the training data
f = [mu+2*sqrt(s2); flipdim(mu-2*sqrt(s2),1)];
fill([xs; flipdim(xs,1)], f, [7 7 7]/8)
hold on;
plot(xs, mu);
plot(x, y, '+')


