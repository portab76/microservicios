package com.proyectocamaras.auth.test;
/*
 * Generador de Contraseñas Encriptadas
 * Crear versiones encriptadas seguras de contraseñas para almacenar en la base de datos
 */
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import java.util.Scanner;

public class BCryptGenerator {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Ingrese la contraseña a encriptar: ");
        String rawPassword = scanner.nextLine();
        
        PasswordEncoder passwordEncoder = new BCryptPasswordEncoder();
        String encodedPassword = passwordEncoder.encode(rawPassword);
        
        System.out.println("Contraseña encriptada: " + encodedPassword);
        scanner.close();
    }
}
