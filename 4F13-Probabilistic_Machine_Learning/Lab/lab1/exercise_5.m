% Loading data for coursework1-a
data = load('cw1e.mat');
x = data.x;
y = data.y;
n_train = size(x,1);
sq_train = sqrt(n_train);

% Building test points
x_aux = -3:0.3:3;
sq_test = size(x_aux,2);
n_test = sq_test^2;
[x_aux,y_aux] = meshgrid(x_aux);
x_aux = reshape(x_aux,n_test,1);
y_aux = reshape(y_aux,n_test,1);
xs = [x_aux y_aux];

%mesh(reshape(x(:,1),11,11),reshape(x(:,2),11,11),reshape(y,11,11));

% We need specify the mean, covariance and likelihood functions
meanfunc = [];              % empty: don't use a mean function
likfunc = @likGauss;        % Gaussian likelihood

%% First GP model
covfunc1 = @covSEard;
hyp1 = struct('mean', [], 'cov', [0 0 0], 'lik', 0);
% Set hyperparameters by optimizing the (log) marginal likelihood
hyp1_2 = minimize(hyp1, @gp, -100, @infGaussLik, meanfunc, covfunc1, likfunc, x, y);

nlZ1 = gp(hyp1_2, @infGaussLik, meanfunc, covfunc1, likfunc, x, y);

fprintf('Negative Log Likelihood value at optimized hyperparams (GP1): %f\n', nlZ1);

[mu_1 s2_1] =  gp(hyp1_2, @infGaussLik, meanfunc, covfunc1, likfunc, x, y, xs);

%subplot(2,1,1);
mesh(reshape(xs(:,1),sq_test,sq_test),reshape(xs(:,2),sq_test,sq_test),reshape(mu_1,sq_test,sq_test));
hold on;
mesh(reshape(xs(:,1),sq_test,sq_test),reshape(xs(:,2),sq_test,sq_test),reshape(mu_1+2*sqrt(s2_1),sq_test,sq_test));
hold on;
mesh(reshape(xs(:,1),sq_test,sq_test),reshape(xs(:,2),sq_test,sq_test),reshape(mu_1-2*sqrt(s2_1),sq_test,sq_test));
%subplot(2,1,2);
%mesh(reshape(x(:,1),sq_train,sq_train),reshape(x(:,2),sq_train,sq_train),reshape(y,sq_train,sq_train));

%% Second GP model
covfunc2 = {@covSum, {@covSEard, @covSEard}};
hyp2 = struct('mean', [], 'cov', 0.1*randn(6,1), 'lik', 0);

% Set hyperparameters by optimizing the (log) marginal likelihood
hyp2_2 = minimize(hyp2, @gp, -100, @infGaussLik, meanfunc, covfunc2, likfunc, x, y);

nlZ2 = gp(hyp1_2, @infGaussLik, meanfunc, covfunc1, likfunc, x, y);

fprintf('Negative Log Likelihood value at optimized hyperparams (GP2): %f\n', nlZ2);

[mu_2 s2_2] =  gp(hyp2_2, @infGaussLik, meanfunc, covfunc2, likfunc, x, y, xs);