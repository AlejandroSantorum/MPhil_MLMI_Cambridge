%% Loading data for coursework1-a,b
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

%% Specify support of hyperparameter search ("GridSearch")
cov = [0.1 exp(1); 0.7 0.5; 0.1 100; 0.7 5; 0.1 1000; 1 exp(1)];

%% Training changing initial hyperparameters
nsubplot = 0;
for i = 1:size(cov,1)
    % Set initial hyperparams
    hyp = struct('mean', [], 'cov', [log(cov(i,1)) log(cov(i,2))], 'lik', 0);

    % Set hyperparameters by optimizing the (log) marginal likelihood
    hyp2 = minimize(hyp, @gp, -100, @infGaussLik, meanfunc, covfunc, likfunc, x, y);

    % Make predictions using these hyperparameters
    [mu, s2] = gp(hyp2, @infGaussLik, meanfunc, covfunc, likfunc, x, y, xs);

    % Plotting
    nsubplot = nsubplot+1;
    subplot(3,2,nsubplot);
    f = [mu+2*sqrt(s2); flip(mu-2*sqrt(s2),1)];
    fill([xs; flip(xs,1)], f, [7 7 7]/8)
    hold on;
    plot(xs, mu);
    plot(x, y, '+')
    xlabel("x");
    ylabel("y");
    title(nsubplot+") Lengthscale: "+cov(i,1)+" , Amplitude: "+cov(i,2));
end

sgtitle('Data fit for different hyperparameter values') 
