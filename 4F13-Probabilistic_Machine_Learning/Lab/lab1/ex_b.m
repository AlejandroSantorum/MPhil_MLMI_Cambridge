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

%% Specify support of hyperparameter search ("GridSearch")
cov_log_ls = [-1 1];
cov_log_ns = [-1 1];

%% Training changing initial hyperparameters
nsubplot = 0;
for i = 1:length(cov_log_ls)
    for j = 1:length(cov_log_ns)
        % Set initial hyperparams
        hyp = struct('mean', [], 'cov', [cov_log_ls(i) cov_log_ns(j)], 'lik', 0);
        
        % Set hyperparameters by optimizing the (log) marginal likelihood
        hyp2 = minimize(hyp, @gp, -100, @infGaussLik, meanfunc, covfunc, likfunc, x, y);
        
        % Make predictions using these hyperparameters
        [mu, s2] = gp(hyp2, @infGaussLik, meanfunc, covfunc, likfunc, x, y, xs);
        
        % Plotting
        nsubplot = nsubplot+1;
        subplot(2,2,nsubplot);
        f = [mu+2*sqrt(s2); flip(mu-2*sqrt(s2),1)];
        fill([xs; flip(xs,1)], f, [7 7 7]/8)
        hold on;
        plot(xs, mu);
        plot(x, y, '+')
        title("Lengthscale: "+cov_log_ls(i)+" , Noise: "+cov_log_ns(i));
    end
end

sgtitle('Data fit for different hyperparameter values') 
