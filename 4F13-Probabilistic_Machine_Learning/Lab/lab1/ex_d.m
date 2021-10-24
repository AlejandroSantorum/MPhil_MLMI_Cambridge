%% Create data
n = 200;
x = linspace(-5, 5, n)';


%% Specify the mean, covariance and likelihood functions
meanfunc = [];              % empty: don't use a mean function
covfunc = {@covProd, {@covPeriodic, @covSEiso}};
likfunc = @likGauss;        % Gaussian likelihood

%% Init the hyperparameters
%   first 3 hyperparams for covPeriodic func: [ln(lengthscale), ln(period), ln(sigma)]
%   last 2 hyperparams for covSEiso func: [ln(lengthscale), ln(sigma)]
hyp.cov = [-0.5 0 0 2 0];

%% Generating random (essentially) noise free functions
% Eval covariance matrix K
K = feval(covfunc{:}, hyp.cov, x);
% Generate function values
K = K + 1e-6*eye(n);
n_functions = 3;
y = chol(K)'*gpml_randn(0.15, n, n_functions);

%% Plotting sampled functions
plot(x, y)
ylim([-3 3])

