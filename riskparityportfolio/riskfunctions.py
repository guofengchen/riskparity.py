import jax.numpy as np
from jax import grad, jit

class RiskConcentrationFunction:
    def __init__(self, portfolio):
        self.portfolio = portfolio

    def evaluate(self):
        return np.sum(np.square(self.risk_concentration_vector()))

    # the vector g in Feng & Palomar 2015
    def risk_concentration_vector(self, portfolio_weights):
        raise NotImplementedError("this method should be implemented in the child class")

    # jacobian of the vector function risk_concentration_vector with respect to weights
    def jacobian_risk_concentration_vector(self):
        return jit(grad(risk_concentration_vector(argnums=1)))

class RiskContribOverBudgetDoubleIndex(RiskConcentrationFunction):
    def risk_concentration_vector(self, portfolio_weights):
        N = len(portfolio_weights)
        marginal_risk = np.multiply(portfolio_weights,
                np.matmul(self.portfolio.covariance, portfolio_weights))
        normalized_marginal_risk = marginal_risk / self.portfolio.budget
        return np.tile(normalized_marginal_risk, [N]) - repeat(normalized_marginal_risk, N)


class RiskContribOverVarianceMinusBudget(RiskConcentrationFunction):
    def risk_concentration_vector(self, portfolio_weights):
        marginal_risk = np.multiply(self.portfolio.weights,
                np.matmul(self.portfolio.covariance, portfolio_weights))
        return marginal_risk / np.sum(marginal_risk) - self.portfolio.budget
