CREATE TABLE estudiantes (
  rut VARCHAR(12) PRIMARY KEY,
  nombre_completo VARCHAR(100),
  edad INT,
  curso VARCHAR(50)
);

CREATE TABLE evaluaciones (
  id INT AUTO_INCREMENT PRIMARY KEY,
  rut_estudiante VARCHAR(12),
  semestre VARCHAR(50),
  asignatura VARCHAR(50),
  evaluacion FLOAT,
  FOREIGN KEY (rut_estudiante) REFERENCES estudiantes(rut)
);
