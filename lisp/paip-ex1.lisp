; Exercise 1.1 [m] Define a version of last-name that handles "Rex Morgan MD," 
; "Morton Downey, Jr.," and whatever other cases you can think of.

(defun last-name (name)
    "Return the last name of given name"
    (car (last name))
)

(print (last-name '(Enix Yu)))

; Exercise 1.2 [m] Write a function to exponentiate, or raise a number to an 
; integer power. For example: (power 3 2) = 9.

(defun power (x y)
    "Return the y power of x"
    (if (equal y 1) 
        x 
        (* x (power x (- y 1)))
    )
)

(print (power 4 5))  ; 4^5 = 1024

; Exercise 1.3 [m] Write a function that counts the number of atoms in an expression. 
; For example: (count-atoms '(a (b) c)) = 3. Notice that there is something of an 
; ambiguity in this: should (a nil c) count as three atoms, or as two, because it 
; is equivalent to (a () c)?

(defun flattern (expr)
    "Return a flattern list for expr"
    (if (typep expr 'list)
        (if (>= (length expr) 2)
            (append (flattern (first expr)) (flattern (rest expr)))
            (if (>= (length expr) 1)
                (flattern (first expr))
                (list expr)
            )
        )
        (list expr)
    )
)

(print (flattern '(1 2 1 (1) (((1))))))  ; '(1 2 1 1 1)

(defun count-atoms (expr)
    "Return the number of atoms in given expr"
    (length (flattern expr))
)

(print (count-atoms '(1 2 1 (1) (((1))))))  ;5


; Exercise 1.4 [m] Write a function that counts the number of times an expression occurs 
; anywhere within another expression. Example: (count-anywhere 'a '(a ((a) b) a)) => 3.

(defun count-anywhere (candidate seq)
    "Counts the number of times candidate occurs within seq"
    (apply #'+
        (mapcar 
            #'(lambda (x) 
                (if (= x candidate) 
                    1 
                    0
                )
            ) 
            (flattern seq)
        )
    )
)

(print (count-anywhere 1 '(1 2 1 (1) (((1))))))  ;4


; Exercise 1.5 [m] Write a function to compute the dot product of two sequences of numbers, 
; represented as lists. The dot product is computed by multiplying corresponding elements 
; and then adding up the resulting products. Example:
;
;       (dot-product '(10 20) '(3 4)) = 10 x 3 + 20 x 4 = 110
;

(defun dot-product (seq1 seq2)
    "Dot product of seq1 and seq2"
    (apply #'+ 
        (mapcar #'* seq1 seq2)
    )
)

(print (dot-product '(10 20) '(3 4))) ; 10 x 3 + 20 x 4 = 110
