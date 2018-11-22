;; This is one part of Recurrent Problem
;; 
;; ==================
;; The Tower of Hanoi
;; ==================
;; 
;; Problem:
;; The tower of Hanoi is introduced by French mathematician
;; Edouard Lucas in 1883.
;; Suppose we have given a tower of eight disks, initialy stacking in
;; decreasing size on one of three pegs:
;; 
;; 
;;          |                       |                       |
;;         [|]                      |                       |
;;        [ | ]                     |                       |
;;       [  |  ]                    |                       |
;;      [   |   ]                   |                       |
;;     [    |    ]                  |                       |
;;    [     |     ]                 |                       |
;;   [      |      ]                |                       |
;;  [       |       ]               |                       |
;; ===================     ===================     ===================
;;         peg1                    peg2                    peg3
;; 
;; The objective is to tranfer the entire tower to one of the other pegs,
;; moving only one disk at a time and never moving a larger one onto a
;; smaller.
;; 
;; So, how many steps are needed to achive this goal?
;; 
;; 
;; Analyst:
;; 
;; Let's define T(n) is the number of steps to move n disks to another peg
;; When n = 0, no step is needed, so T(0) = 0
;; When n = 1, we only need one move to achive the goal, so T(1) = 1
;; When n = 2, we need three steps to finish the job, so T(2) = 3 
;; 
;; When we need to move n disks, we first need to move n - 1 disks to one peg,
;; and move the nth disk to another peg, and then move n - 1 disks to that peg,
;; so:
;;                      T(0) = 0
;;                      T(n) = 2 * T(n - 1) + 1, when n > 0
;;

(defun steps-for-tower-hanoi (n)
    "Return the total steps to move n disks to another peg"
    (if (eq n 0)
        0
        (+ (* 2 (steps-for-tower-hanoi (- n 1))) 1)
    )
)

(defun forloop (fn from end step)
    "Iterate from `from` to `end` with `step`, and call fn in each loop"
    (funcall fn from)
    (if (< from end)
        (forloop fn (+ from step) end step)
    )
)

(defun print-tower-hanoi (n)
    "Print the steps for n disks tower of hanoi"
    (print (format nil "Total moves for ~D disk(s) of Tower of Hanoi = ~D" n (steps-for-tower-hanoi n)))
)

(forloop #'print-tower-hanoi 0 8 1)
(print-tower-hanoi 64) ;; End of the world
