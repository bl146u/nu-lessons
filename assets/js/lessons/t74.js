"use strict";


(($) => {


    $(() => {

        $("#form-lesson-t74 input[name=image]").bind("change", (event) => {
            let target = $(event.currentTarget);
            if (target.val()) target.closest("form").submit();
        })

    })


})(jQuery);
