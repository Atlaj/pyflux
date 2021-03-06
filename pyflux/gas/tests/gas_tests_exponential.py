import numpy as np
import pyflux as pf

# Generate some random data
noise = np.random.normal(0,1,200)
data = np.zeros(200)

for i in range(1,len(data)):
	data[i] = 0.9*data[i-1] + noise[i]

exponentialdata = np.random.exponential(np.exp(data),200)

def test_exponential_no_terms():
	"""
	Tests an GAS model with no AR or SC terms, and that
	the latent variable list length is correct, and that the estimated
	latent variables are not nan
	"""
	model = pf.GAS(data=exponentialdata, ar=0, sc=0, family=pf.Exponential())
	x = model.fit()
	assert(len(model.latent_variables.z_list) == 1)
	lvs = np.array([i.value for i in model.latent_variables.z_list])
	assert(len(lvs[np.isnan(lvs)]) == 0)

def test_exponential_couple_terms():
	"""
	Tests an GAS model with 1 AR and 1 SC term and that
	the latent variable list length is correct, and that the estimated
	latent variables are not nan
	"""
	model = pf.GAS(data=exponentialdata, ar=1, sc=1, family=pf.Exponential())
	x = model.fit()
	assert(len(model.latent_variables.z_list) == 3)
	lvs = np.array([i.value for i in model.latent_variables.z_list])
	assert(len(lvs[np.isnan(lvs)]) == 0)

def test_exponential_couple_terms_integ():
	"""
	Tests an GAS model with 1 AR and 1 SC term, integrated once, and that
	the latent variable list length is correct, and that the estimated
	latent variables are not nan
	"""
	model = pf.GAS(data=exponentialdata, ar=1, sc=1, integ=1, family=pf.Exponential())
	x = model.fit()
	assert(len(model.latent_variables.z_list) == 3)
	lvs = np.array([i.value for i in model.latent_variables.z_list])
	assert(len(lvs[np.isnan(lvs)]) == 0)

def test_exponential_bbvi():
	"""
	Tests an GAS model estimated with BBVI and that the length of the latent variable
	list is correct, and that the estimated latent variables are not nan
	"""
	model = pf.GAS(data=exponentialdata, ar=1, sc=1, family=pf.Exponential())
	x = model.fit('BBVI',iterations=100, map_start=False)
	assert(len(model.latent_variables.z_list) == 3)
	lvs = np.array([i.value for i in model.latent_variables.z_list])
	assert(len(lvs[np.isnan(lvs)]) == 0)

def test_exponential_bbvi_mini_batch():
    """
    Tests an ARIMA model estimated with BBVI and that the length of the latent variable
    list is correct, and that the estimated latent variables are not nan
    """
    model = pf.GAS(data=exponentialdata, ar=1, sc=1, family=pf.Exponential())
    x = model.fit('BBVI',iterations=200, mini_batch=32, map_start=False)
    assert(len(model.latent_variables.z_list) == 3)
    lvs = np.array([i.value for i in model.latent_variables.z_list])
    assert(len(lvs[np.isnan(lvs)]) == 0)

def test_exponential_bbvi_elbo():
    """
    Tests that the ELBO increases
    """
    model = pf.GAS(data=exponentialdata, ar=1, sc=1, family=pf.Exponential())
    x = model.fit('BBVI',iterations=200, record_elbo=True, map_start=False)
    assert(x.elbo_records[-1]>x.elbo_records[0])

def test_exponential_bbvi_mini_batch_elbo():
    """
    Tests that the ELBO increases
    """
    model = pf.GAS(data=exponentialdata, ar=1, sc=1, family=pf.Exponential())
    x = model.fit('BBVI',iterations=100, mini_batch=32, record_elbo=True, map_start=False)
    assert(x.elbo_records[-1]>x.elbo_records[0])

def test_exponential_mh():
	"""
	Tests an GAS model estimated with Metropolis-Hastings and that the length of the 
	latent variable list is correct, and that the estimated latent variables are not nan
	"""
	model = pf.GAS(data=exponentialdata, ar=1, sc=1, family=pf.Exponential())
	x = model.fit('M-H',nsims=300)
	assert(len(model.latent_variables.z_list) == 3)
	lvs = np.array([i.value for i in model.latent_variables.z_list])
	assert(len(lvs[np.isnan(lvs)]) == 0)

def test_exponential_laplace():
	"""
	Tests an GAS model estimated with Laplace approximation and that the length of the 
	latent variable list is correct, and that the estimated latent variables are not nan
	"""
	model = pf.GAS(data=exponentialdata, ar=1, sc=1, family=pf.Exponential())
	x = model.fit('Laplace')
	assert(len(model.latent_variables.z_list) == 3)
	lvs = np.array([i.value for i in model.latent_variables.z_list])
	assert(len(lvs[np.isnan(lvs)]) == 0)

def test_exponential_pml():
	"""
	Tests a PML model estimated with Laplace approximation and that the length of the 
	latent variable list is correct, and that the estimated latent variables are not nan
	"""
	model = pf.GAS(data=exponentialdata, ar=1, sc=1, family=pf.Exponential())
	x = model.fit('PML')
	assert(len(model.latent_variables.z_list) == 3)
	lvs = np.array([i.value for i in model.latent_variables.z_list])
	assert(len(lvs[np.isnan(lvs)]) == 0)

def test_exponential_predict_length():
	"""
	Tests that the prediction dataframe length is equal to the number of steps h
	"""
	model = pf.GAS(data=exponentialdata, ar=2, sc=2, family=pf.Exponential())
	x = model.fit()
	x.summary()
	assert(model.predict(h=5).shape[0] == 5)

def test_exponential_predict_is_length():
	"""
	Tests that the prediction IS dataframe length is equal to the number of steps h
	"""
	model = pf.GAS(data=exponentialdata, ar=2, sc=2, family=pf.Exponential())
	x = model.fit()
	assert(model.predict_is(h=5).shape[0] == 5)

def test_exponential_predict_nans():
	"""
	Tests that the predictions are not nans
	"""
	model = pf.GAS(data=exponentialdata, ar=2, sc=2, family=pf.Exponential())
	x = model.fit()
	x.summary()
	assert(len(model.predict(h=5).values[np.isnan(model.predict(h=5).values)]) == 0)

def test_exponential_predict_is_nans():
	"""
	Tests that the in-sample predictions are not nans
	"""
	model = pf.GAS(data=exponentialdata, ar=2, sc=2, family=pf.Exponential())
	x = model.fit()
	x.summary()
	assert(len(model.predict_is(h=5).values[np.isnan(model.predict_is(h=5).values)]) == 0)

def test_exponential_predict_nonconstant():
    """
    We should not really have predictions that are constant (should be some difference)...
    This captures bugs with the predict function not iterating forward
    """
    model = pf.GAS(data=exponentialdata, ar=1, sc=1, family=pf.Exponential())
    x = model.fit()
    predictions = model.predict(h=10, intervals=False)
    assert(not np.all(predictions.values==predictions.values[0]))
    
def test_exponential_predict_is_nonconstant():
    """
    We should not really have predictions that are constant (should be some difference)...
    This captures bugs with the predict function not iterating forward
    """
    model = pf.GAS(data=exponentialdata, ar=1, sc=1, family=pf.Exponential())
    x = model.fit()
    predictions = model.predict_is(h=10, intervals=False)
    assert(not np.all(predictions.values==predictions.values[0]))
    
def test_exponential_predict_intervals():
    """
    Tests prediction intervals are ordered correctly
    """
    model = pf.GAS(data=exponentialdata, ar=1, sc=1, family=pf.Exponential())
    x = model.fit()
    predictions = model.predict(h=10, intervals=True)

    assert(np.all(predictions['99% Prediction Interval'].values > predictions['95% Prediction Interval'].values))
    assert(np.all(predictions['95% Prediction Interval'].values > predictions['5% Prediction Interval'].values))
    assert(np.all(predictions['5% Prediction Interval'].values > predictions['1% Prediction Interval'].values))

def test_exponential_predict_is_intervals():
    """
    Tests prediction intervals are ordered correctly
    """
    model = pf.GAS(data=exponentialdata, ar=1, sc=1, family=pf.Exponential())
    x = model.fit()
    predictions = model.predict_is(h=10, intervals=True)
    assert(np.all(predictions['99% Prediction Interval'].values > predictions['95% Prediction Interval'].values))
    assert(np.all(predictions['95% Prediction Interval'].values > predictions['5% Prediction Interval'].values))
    assert(np.all(predictions['5% Prediction Interval'].values > predictions['1% Prediction Interval'].values))

def test_exponential_predict_intervals_bbvi():
    """
    Tests prediction intervals are ordered correctly
    """
    model = pf.GAS(data=exponentialdata, ar=1, sc=1, family=pf.Exponential())
    x = model.fit('BBVI', iterations=100)
    predictions = model.predict(h=10, intervals=True)

    assert(np.all(predictions['99% Prediction Interval'].values > predictions['95% Prediction Interval'].values))
    assert(np.all(predictions['95% Prediction Interval'].values > predictions['5% Prediction Interval'].values))
    assert(np.all(predictions['5% Prediction Interval'].values > predictions['1% Prediction Interval'].values))

def test_exponential_predict_is_intervals_bbvi():
    """
    Tests prediction intervals are ordered correctly
    """
    model = pf.GAS(data=exponentialdata, ar=1, sc=1, family=pf.Exponential())
    x = model.fit('BBVI', iterations=100)
    predictions = model.predict_is(h=10, intervals=True)
    assert(np.all(predictions['99% Prediction Interval'].values > predictions['95% Prediction Interval'].values))
    assert(np.all(predictions['95% Prediction Interval'].values > predictions['5% Prediction Interval'].values))
    assert(np.all(predictions['5% Prediction Interval'].values > predictions['1% Prediction Interval'].values))

def test_exponential_predict_intervals_mh():
    """
    Tests prediction intervals are ordered correctly
    """
    model = pf.GAS(data=exponentialdata, ar=1, sc=1, family=pf.Exponential())
    x = model.fit('M-H', nsims=400)
    predictions = model.predict(h=10, intervals=True)

    assert(np.all(predictions['99% Prediction Interval'].values > predictions['95% Prediction Interval'].values))
    assert(np.all(predictions['95% Prediction Interval'].values > predictions['5% Prediction Interval'].values))
    assert(np.all(predictions['5% Prediction Interval'].values > predictions['1% Prediction Interval'].values))

def test_exponential_predict_is_intervals_mh():
    """
    Tests prediction intervals are ordered correctly
    """
    model = pf.GAS(data=exponentialdata, ar=1, sc=1, family=pf.Exponential())
    x = model.fit('M-H', nsims=400)
    predictions = model.predict_is(h=10, intervals=True)
    assert(np.all(predictions['99% Prediction Interval'].values > predictions['95% Prediction Interval'].values))
    assert(np.all(predictions['95% Prediction Interval'].values > predictions['5% Prediction Interval'].values))
    assert(np.all(predictions['5% Prediction Interval'].values > predictions['1% Prediction Interval'].values))

def test_exponential_sample_model():
    """
    Tests sampling function
    """
    model = pf.GAS(data=exponentialdata, ar=1, sc=1, family=pf.Exponential())
    x = model.fit('BBVI', iterations=100)
    sample = model.sample(nsims=100)
    assert(sample.shape[0]==100)
    assert(sample.shape[1]==len(data)-1)

def test_exponential_ppc():
    """
    Tests PPC value
    """
    model = pf.GAS(data=exponentialdata, ar=1, sc=1, family=pf.Exponential())
    x = model.fit('BBVI', iterations=100)
    p_value = model.ppc()
    assert(0.0 <= p_value <= 1.0)

