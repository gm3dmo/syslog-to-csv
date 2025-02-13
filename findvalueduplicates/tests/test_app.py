import pytest
from app import app, parse_log_line

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test that home page loads successfully"""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Log File Analyzer' in rv.data

def test_parse_log_line_with_duplicates():
    """Test parsing a log line with known duplicates"""
    test_line = 'app=github env=production enterprise=true enterprise1=true x_real_ip=10.0.0.1 x_forwarded_for=10.0.0.1'
    result = parse_log_line(test_line)
    
    assert 'true' in result
    assert '10.0.0.1' in result
    assert result['true']['count'] == 2
    assert result['10.0.0.1']['count'] == 2
    assert 'enterprise' in result['true']['keys']
    assert 'enterprise1' in result['true']['keys']
    assert 'x_real_ip' in result['10.0.0.1']['keys']
    assert 'x_forwarded_for' in result['10.0.0.1']['keys']

def test_parse_log_line_no_duplicates():
    """Test parsing a log line with no duplicates"""
    test_line = 'app=github env=production status=200'
    result = parse_log_line(test_line)
    assert result == {}

def test_parse_log_line_with_quoted_values():
    """Test parsing a log line with quoted values"""
    test_line = 'path="/api/v3" message="Hello World" error="Hello World"'
    result = parse_log_line(test_line)
    assert 'Hello World' in result
    assert result['Hello World']['count'] == 2
    assert 'message' in result['Hello World']['keys']
    assert 'error' in result['Hello World']['keys']

def test_analyze_endpoint(client):
    """Test the /analyze endpoint"""
    test_data = {
        'line': 'app=github env=production enterprise=true enterprise1=true'
    }
    response = client.post('/analyze', json=test_data)
    assert response.status_code == 200
    result = response.get_json()
    assert 'true' in result
    assert result['true']['count'] == 2
    assert 'enterprise' in result['true']['keys']
    assert 'enterprise1' in result['true']['keys']

def test_analyze_endpoint_empty_line(client):
    """Test the /analyze endpoint with empty line"""
    test_data = {'line': ''}
    response = client.post('/analyze', json=test_data)
    assert response.status_code == 200
    assert response.get_json() == {}

def test_parse_log_line_with_nil_values():
    """Test parsing a log line with nil values - these should be excluded from duplicates"""
    test_line = 'query_string=nil parent_installation_id=nil other=value'
    result = parse_log_line(test_line)
    assert result == {}

def test_parse_complex_log_line():
    """Test parsing a complex log line with mixed quoted and unquoted values"""
    test_line = '''app=github env=production auth_fingerprint="token:123" x_real_ip=10.0.0.1 x_forwarded_for=10.0.0.1 status=201 message="Success" error="Success"'''
    result = parse_log_line(test_line)
    
    assert '10.0.0.1' in result
    assert 'Success' in result
    assert result['10.0.0.1']['count'] == 2
    assert result['Success']['count'] == 2 