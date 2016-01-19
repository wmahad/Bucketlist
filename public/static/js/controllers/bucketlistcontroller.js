'use strict';


app.controller('BucketListController', 
	function BucketListController($rootScope, $scope, $state, $localStorage,$stateParams, BucketListService) {
		$(document).ready(function(){
		    // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
		    $('.modal-trigger').leanModal();
		});
		var BlService = BucketListService;

		$scope.username = $localStorage.currentUser;

		//get bucketlist data
		$scope.Bucketlists = BlService.Bucketlists.getAllBuckets();


		$scope.openModal = function (bucketlist_id) {
			$scope.singlebucketlist = BlService.Bucketlists.getOneBucket({id:bucketlist_id});
			$('#modal1').openModal();
		};

		//create a new bucketlist
		$scope.createBucketlist = function () {
			var data = {
				name:$scope.newbucket.name
				// , 
				// created_by:$cookies.get('id')
			};
			BlService.Bucketlists.createBucket(data).
		    $promise
	        .then(function (response) {
				$state.go('dashboard', {}, {reload:true});
	        })
	        .catch(function(responseError){
	            console.log(responseError);
	        });
			
		};

		//update bucketlist
		$scope.updateBucketlist = function (_id) {
			var data = {
				name: $scope.bucketedit.name, 
				// created_by:$cookies.get('id'),
				id: _id
			};
			console.log(data);
			BlService.Bucketlists.updateBucket(data)
			.$promise
			.then(function (response) {
				$state.go('dashboard', {}, {reload: true});
				$('#modal1').closeModal();
			})
			.catch(function (responseError) {
				// body...
			});
			
		};

		//delete individual bucketlist
		$scope.deleteBucketlist = function (bucket) {
			bucket.$deleteBucket().then(function (){
				$state.go('dashboard', {}, {reload:true});
			});
		};	
	}
);



app.controller('BucketListViewController', 
	function BucketListViewController ($rootScope, $scope, $state, $localStorage, $stateParams, BucketListService) {
		$(document).ready(function(){
		    // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
		    $('.modal-trigger').leanModal();
		}); 

		$scope.username = $localStorage.currentUser;
		$scope.BucketlistItem = BucketListService.Bucketlists.getOneBucket({ id: $stateParams.id });

		$scope.openItemModal = function (bucketlist_id, item_id) {
			var data ={
				bid: bucketlist_id,
				id: item_id
			};
			$scope.single_item = BucketListService.BucketlistItems.getOneBucketItem(data);
			$('#modal1').openModal();
		};

		$scope.createBucketItem = function (url_params) {
			BucketListService.BucketlistItems.createBucketItem(url_params)
            .$promise
            .then(  
                function (response) {
                    $state.go('viewBucket', {id:url_params.bid}, {reload:true});
                }
            );
		};

		$scope.deleteItem =function (url_params) {
			BucketListService.BucketlistItems.deleteBucketItem(url_params)
            .$promise
            .then(  
                function (response) {
                    $state.go('viewBucket', {id:url_params.bid}, {reload:true});
                }
            );
		};

		$scope.editItem =function (_id, b_id) {
			var data = {
				name: $scope.itemedit.name,
				done: $scope.itemedit.done,
				id: _id,
				bucketlist : b_id,
				bid: b_id
			};
			BucketListService.BucketlistItems.updateBucketItem(data)
            .$promise
            .then(  
                function (response) {
                    $state.go('viewBucket', {id:b_id}, {reload:true});
                    $('#modal1').closeModal();
                }
            );
		};

	}
);