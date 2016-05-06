'use strict';


app.controller('AuthController', 
	function AuthController($rootScope, $scope, $state, $localStorage, BucketListService, toastr) {

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
                toastr.success('Welcome ' + $scope.user.username);
            })
            .catch(function(responseError){
                toastr.error('Invalid credentials');
            });

		};

		$scope.register = function () {
			var data = {username: $scope.user.username, password: $scope.user.password};
			BlService.users.create(data).
		    $promise
	        .then($scope.login)
	        .catch(function(responseError){
	            toastr.error('Could not register user');
	        });
			
		};

	}
);



