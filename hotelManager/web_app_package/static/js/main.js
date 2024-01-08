/*  ---------------------------------------------------
  Template Name: Hiroto
  Description:  Hiroto Hotel HTML Template
  Author: Colorlib
  Author URI: https://colorlib.com
  Version: 1.0
  Created: Colorlib
---------------------------------------------------------  */

'use strict';

(function ($) {

    /*------------------
        Preloader
    --------------------*/
    $(window).on('load', function () {
        $(".loader").fadeOut();
        $("#preloder").delay(200).fadeOut("slow");
    });

    /*------------------
        Background Set
    --------------------*/
    $('.set-bg').each(function () {
        var bg = $(this).data('setbg');
        $(this).css('background-image', 'url(' + bg + ')');
    });

    //Canvas Menu
    $(".canvas__open").on('click', function () {
        $(".offcanvas-menu-wrapper").addClass("active");
        $(".offcanvas-menu-overlay").addClass("active");
    });

    $(".offcanvas-menu-overlay").on('click', function () {
        $(".offcanvas-menu-wrapper").removeClass("active");
        $(".offcanvas-menu-overlay").removeClass("active");
    });

    /*------------------
		Navigation
	--------------------*/
    $(".menu__class").slicknav({
        appendTo: '#mobile-menu-wrap',
        allowParentLinks: true
    });

    /*--------------------------
        Gallery Slider
    ----------------------------*/
    $(".gallery__slider").owlCarousel({
        loop: true,
        margin: 10,
        items: 4,
        dots: false,
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true,
        responsive: {
            992: {
                items: 4
            },
            768: {
                items: 3
            },
            576: {
                items: 2
            },
            0: {
                items: 1
            }
        }
    });

    /*--------------------------
        Room Pic Slider
    ----------------------------*/
    $(".room__pic__slider").owlCarousel({
        loop: true,
        margin: 0,
        items: 1,
        dots: false,
        nav: true,
        navText: ["<i class='arrow_carrot-left'></i>", "<i class='arrow_carrot-right'></i>"],
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: false
    });

    /*--------------------------
        Room Details Pic Slider
    ----------------------------*/
    $(".room__details__pic__slider").owlCarousel({
        loop: true,
        margin: 10,
        items: 2,
        dots: false,
        nav: true,
        navText: ["<i class='arrow_carrot-left'></i>", "<i class='arrow_carrot-right'></i>"],
        autoHeight: false,
        autoplay: false,
        mouseDrag: false,
        responsive: {
            576: {
                items: 2
            },
            0: {
                items: 1
            }
        }
    });
    
    /*--------------------------
        Testimonial Slider
    ----------------------------*/
    var testimonialSlider = $(".testimonial__slider");
    testimonialSlider.owlCarousel({
        loop: true,
        margin: 30,
        items: 1,
        dots: true,
        nav: true,
        navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true,
        mouseDrag: false,
        onInitialized: function(e) {
        	    var a = this.items().length;
                $("#snh-1").html("<span>01</span><span>" + "0" + a + "</span>");
                var presentage = Math.round((100 / a));
                $('.slider__progress span').css("width", presentage + "%");
                
            }
        }).on("changed.owl.carousel", function(e) {
            var b = --e.item.index, a = e.item.count;
            $("#snh-1").html("<span> "+ "0" +(1 > b ? b + a : b > a ? b - a : b) + "</span><span>" + "0" + a + "</span>");

            var current = e.page.index + 1;
            var presentage = Math.round((100 / e.page.count) * current);
            $('.slider__progress span').css("width", presentage + "%");
    });
    
    
    /*--------------------------
        Logo Slider
    ----------------------------*/
    $(".logo__carousel").owlCarousel({
        loop: true,
        margin: 100,
        items: 5,
        dots: false,
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: false,
        responsive: {
            992: {
                items: 5
            },
            768: {
                items: 3
            },
            320: {
                items: 2
            },
            0: {
                items: 1
            }
        }
    });

    /*--------------------------
        Select
    ----------------------------*/
    $("select").niceSelect();
    

    /*--------------------------
        Datepicker
    ----------------------------*/
    var today = new Date(); 
    var dd = today.getDate(); 
    var mm = today.getMonth() + 1; 

    var yyyy = today.getFullYear(); 
    if (dd < 10) { 
        dd = '0' + dd; 
    }
    var mS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

    var month;

    for (let i = 0; i <= 12; i++) {
        const element = mS[i];
        if (mm == mS.indexOf(mS[i])) {
            month = mS[i-1];
        }
    }
    var today = dd + ' ' + month + ' ' + yyyy; 

    $(".check__in").val(today);
    $(".check__out").val(today);

    $( ".datepicker_pop" ).datepicker({ 
        dateFormat: 'dd M yy',
        minDate: 0
    });

})(jQuery);
    // Chọn phòng
function changeColor(element, room_name) {
    element.classList.toggle('bg-info');

    var inputRoom = document.getElementById('rooms');
    var numRoomIp = (document.getElementById('numRoom').textContent);
    var numRoom = parseInt(numRoomIp)
    var tempString = inputRoom.value;
    // Kiểm tra xem chuỗi có tồn tại trong input không
    var isExist = tempString.includes(room_name);
    // Nếu chuỗi đã tồn tại, loại bỏ nó; ngược lại, thêm vào
    if (isExist) {
        tempString = tempString.replace(room_name+" ", '');
        numRoom = numRoom - 1;
    } else {
        tempString += room_name + ' ';
        numRoom = numRoom + 1;
    }
    // Gán giá trị mới vào input
    inputRoom.value = tempString;
    document.getElementById('numRoom').textContent = numRoom
}

function checkCustomerWithRoom(id, name, price) {
    // Lấy giá trị từ input A và B Chuyển đổi giá trị thành số
    var numOfCus = parseFloat(document.getElementById('numOfGuests').value) ;
    var numRoom = parseFloat(document.getElementById('numRoom').textContent) ;
    var capacity = parseInt(document.getElementById('capacity').textContent) ;

    //Kiểm tra nếu A > B, yêu cầu nhập lại giá trị B
    if (isNaN(numRoom) || isNaN(numOfCus) || (numRoom * capacity) < numOfCus) {
        document.getElementById('numOfGuests').value = ''
        alert('Số khách vượt quá mức quy định');
    } else {
        var rooms = String(document.getElementById('rooms').value)
        fetch('/booking2')
        fetch('/api/book_room', {
        method: "post",
        body: JSON.stringify({
            "rooms": rooms,
        }),
        headers: {
            'Content-Type': "application/json"
        }
    })
}
}
