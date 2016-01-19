'use strict';


app.controller('AuthController', 
	function AuthController($rootScope, $scope, $state, $localStorage, BucketListService) {

		var BlService = BucketListService;

		$scope.login = function(){
		    var data = {username: $scope.user.username, password: $scope.user.password};
		    BlService.auth.login(data).
	        $promise
            .then(function(response){
                $localStorage.token = response.token;
                $localStorage.authenticated = true;
                $localStorage.currentUser = $scope.user.username;
                $localStorage.currentUserid = response.id;

                $state.go('dashboard');
            })
            .catch(function(responseError){
                
            });

		};

		$scope.register = function () {
			var data = {username: $scope.user.username, password: $scope.user.password};
			BlService.users.create(data).
		    $promise
	        .then($scope.login)
	        .catch(function(responseError){
	            //console.log(responseError);
	        });
			
		};

	}
);



