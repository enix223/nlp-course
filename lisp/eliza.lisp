(defun simple-equal (x y)
    "Are x equal to y?"
    (if ((or (atom x) (atom y)))
        (eq x y)
        (and 
            (simple-equal (first x) (first y))
            (simple-equal (rest x) (rest y))
        )
    )
)

;; Exercise 5.1 [s] Would it be a good idea to replace the complex and form in
;; pat-match with the simpler (every #'pat-match pattern input)?
;; 
;; I think it is not good to use every here, cos, every expect sequences as
;; input, and we need pattern input both support atom
(defun pat-match (pattern input)
    "Does pattern match input?"
    (if (variable-p pattern)
        t
        (if (or (atom pattern) (atom input))
            (eq pattern input)
            (and 
                (pat-match (first pattern) (first input))
                (pat-match (rest pattern) (rest input))
            )
        )
    )
)