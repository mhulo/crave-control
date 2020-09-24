<?php

interface IRequest
{
    public function getBody();
}

// Allows access to all $_SERVER properties and $_POST data(for post requests)
class Request Implements IRequest {
  function __construct () {
    $this->bootstrapSelf();
  }
  
  private function bootstrapSelf() {
    foreach ($_SERVER as $key => $value) {
      $this->{$this->toCamelCase($key)} = $value;
    }
  }
  
  private function toCamelCase ($string) {
    $result = strtolower($string);
    preg_match_all('/_[a-z]/', $result, $matches);
    
    foreach ($matches[0] as $match) {
      $c = str_replace('_', '', strtoupper($match));
      $result = str_replace($match, $c, $result);
    }
    
    return $result;
  }
  
  public function getBody() {
    if ($this->requestMethod === 'GET') return;
    
    if ($this->requestMethod === 'POST') {
      $body = new Body();
      
      foreach($_POST as $key => $value) {
        $body->{$key} = filter_input(INPUT_POST, $key, FILTER_SANITIZE_SPECIAL_CHARS);
        $body;
      }
      
      return $body;
    }
  }
  
}

class Body {}

class Router {
  private $result;
  private $supportedRequestMethods = [
    'GET',
    'POST'
  ];
  private $params = [];

  function __construct(IRequest $request) {
    $this->request = $request;
    $this->request->params = null;
  }

  function __call($requestMethod, $args) {
    list($route, $routeHandler) = $args;

    if(!in_array(strtoupper($requestMethod), $this->supportedRequestMethods)) {
      $this->invalidRequestMethodHandler();
    }

    $this->{strtolower($requestMethod)}[$this->formatRoute($route)] = $routeHandler;
  }

  private function formatRoute($route) {
    $route = rtrim($route, '/');
    $path = explode('/', $route);
    $params = [];

    foreach($path as $token) {
      //error_log('token is: ' . $token . ' ' . gettype($token));
      if (substr($token, 0, 1) === '{' and $token[strlen($token) - 1] === '}') {
        $token = ltrim(rtrim($token, '}'), '{');
        array_push($params, $token);
      }
    }

    // Register all routes with and without URL parameters
    if ($params) $this->params[$route] = $params;
    else $this->params[$route] = false;

    return $route === '' ? '/' : $route;
  }
  
  private function mapRequestedRoute($requested_route) {
    $route = rtrim($requested_route, '/');

    //error_log('params:'.print_r($this->params, true));
    //error_log('route:'.print_r($route, true));
    $params = 5;

    // Find routes with params
    if (isset($this->params[$route])) { 
      $params = $this->params[$route];
      error_log('route with params');
    }

    // Route without params
    if ($params === false) {
      return $route === '' ? '/' : $route;
      error_log('route without params');
    }

    //error_log('this->params:' . print_r($this->params, true));

    // Route with params i.e params is null
    foreach ($this->params as $key => $value) {
      if (is_array($this->params[$key])) { // Only routes with params
        $flag = true; // Reset for each iteration
        $store_params = [];
        $store_values = [];

        $stored_path = explode('/', $key);
        $requested_path = explode('/', $route);

        //error_log('requested_path:' . print_r($requested_path, true));
        //error_log('count:' . count($requested_path));
        //error_log('rstored_path:' . print_r($stored_path, true));

        for ($i = 1; (($i < count($requested_path)) && ($i < count($stored_path))); $i++) {
          if ($stored_path[$i][0] === '{' and $stored_path[$i][strlen($stored_path[$i]) - 1] === '}') {
            array_push($store_params, ltrim(rtrim($stored_path[$i], '}'), '{'));
            array_push($store_values, $requested_path[$i]);
            continue;
          }
          else if ($stored_path[$i] !== $requested_path[$i]) {
            $flag = false;
          }
        }
        
        if (($flag === true) and (count($requested_path) === count($stored_path))) {
          // Append params to request object
          for ($i = 0; $i < count($store_params); $i++) {
            //error_log('req:' . print_r($this->request->params, true));
            if (gettype($this->request->params) != 'object') {
              $this->request->params = (object) [];
            }
            $this->request->params->{$store_params[$i]} = $store_values[$i];
          }
          return $key;
        }
      }
    }
  }

  private function invalidRequestMethodHandler() {
    header($this->request->serverProtocol . '405 Method Not Allowed');
  }

  private function defaultRequestHandler() {
    header($this->request->serverProtocol . '404 Not Found');
  }

  function resolve() {
    $requestMethodDictionary = $this->{strtolower($this->request->requestMethod)};
    $formattedRoute = $this->mapRequestedRoute($this->request->requestUri);
    
    //error_log('========');
    //error_log('dict: ' . print_r($requestMethodDictionary, true));
    //error_log('route: ' . gettype($formattedRoute));
    
    if ($formattedRoute != null) {
      $routeHandler = $requestMethodDictionary[$formattedRoute];
      echo call_user_func_array($routeHandler, [$this->request]);
    }
    else {
      return $this->defaultRequestHandler();
    }

  }

  function __destruct() {
    $this->resolve();
  }

}

function useContr($contr, $request)
{
  $controller = explode('@', $contr);
  $contr_file = $controller[0];
  $contr_file_arr = explode('/', $contr_file);
  $contr_class = end($contr_file_arr);
  $contr_meth = $controller[1];

  require_once $contr_file . '.php';
  $res = new $contr_class;
  return $res->$contr_meth($request->params);

}

function useView($view, $request)
{
  $q = $request->params;
  require_once 'views/' . $view . '.php';

}

